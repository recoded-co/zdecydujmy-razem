'use strict';

/* Controllers */

var zdControllers = angular.module('zdControllers', ['ngCookies']);
//'configurations','rates','subjects','posts','geometries','plans',

zdControllers.controller('apiList', ['$scope','$http','$cookies','$rootScope', 'zdServicesFactory','uploadService',
  function($scope,$http,$cookies, $rootScope,zdServicesFactory, uploadService ) {

    $scope.plans = zdServicesFactory.plans.json();
    jsonToNestedCollection(zdServicesFactory.posts.json(),function(data){
        $scope.tree = data;
    });
    $scope.predicate='date';
    $scope.reverse=true;
    $scope.data_arrow=true;

    var post_buff_id = 0;
    $scope.zoom_chase = function(post){
        if(post.parent==null && post_buff_id!=post.id){
            post_buff_id = post.id;
            zdServicesFactory.geometries_content.get({id_param:post.geometry}).$promise.then(function(data){
                map.fitBounds(parseWKTbeta(data.geoelement));
            });
        }
    }

    $scope.scoreUp = function(data){
        data.score = data.score + 1;
        data.sub_rates = true;
        data.positive_rate = data.positive_rate + 1;
        var temp = {
            post: data.id,
            user: configuration.getAuthor(),
            like: true,
            rate: 1
        }
        sendCSRFPost('/zr/api/rates/',$http,$cookies,temp);
    }
    $scope.scoreDown = function(data){
        data.score = data.score - 1;
        data.sub_rates = true;
        data.negative_rate = data.negative_rate -1;
        var temp = {
            post: data.id,
            user: configuration.getAuthor(),
            like: false,
            rate: 1
        }
        sendCSRFPost('/zr/api/rates/',$http,$cookies,temp);
      }

    $scope.delete = function(data) {
        data.text = "";
        data.zmiennac=false;
        };
    $scope.deleteBP = function(base_post) {
        if(base_post)
            base_post.text = "";
        };
    $scope.addDown = function(data) {
            if (data.nodes !== undefined)
                var postCh = data.nodes.length + 1;
            else
                data.nodes = [];
            var temp = {
                author: configuration.getAuthor(),
                parent: data.id,
                plan: configuration.getPlanId(),
                content: data.text,
                geometry: data.geometry || null,
                nodes: [],
                zmiennac:false
            }
            sendTempToServer(temp,$http,$cookies,function(temp){
                data.nodes.unshift(temp);
                data.numcom++;
            });
            data.text = "";
            data.zmiennac=false;
    };
    $scope.showOneDown = function(data){
        if(data.rozwin==undefined || data.rozwin==false){
            data.rozwin=true;
        } else {
            data.rozwin=false;
        }
    };
    $scope.showAll = function(){
          if($scope.showallposts == false){
              $scope.showallposts = true;
          }else{
              $scope.showallposts = false;
          }
      };
    $scope.addVertical = function(data) {
        if (data.nodes !== undefined)
            var postCh = data.nodes.length + 1;
        else
            data.nodes = [];

        var temp = {
            author: configuration.getAuthor(),
            parent: null,
            plan: configuration.getPlanId(),
            content: data.text,
            geometry: null,
            nodes: [],
            zmiennac:false
        }
        sendTempToServer(temp,$http,$cookies,function(temp){
                $scope.tree.push(temp);
            });
        data.text = "";
        data.zmiennac=false;
    };
    //$scope.tree = zdServicesFactory.posts.json();

    $scope.comment = function(data){
        if(userLogedOn($scope.user)){
            data.zmiennac = true;
        }
    };

    //method from outside usage
    $scope.pushCommentIntoScope = function(temp_data,temp_comment){
          var temp = {
            author: configuration.getAuthor(),
            parent: null,
            plan: configuration.getPlanId(),
            content: temp_comment,
            geometry: temp_data.id || null,
            nodes: [],
            zmiennac:false
        }
        sendTempToServer(temp,$http,$cookies,function(temp){
                $scope.tree.push(temp);
            });
          //$scope.tree.$apply();
    };
    $scope.subscribe = function(data, subscribed){
        console.log(data);
        var temp = {
            post: data.id,
            user: parseInt(configuration.getAuthor()),
            active: !subscribed // TODO add variable which says what to do, activate | deactivate
        }
        sendCSRFPost('/zr/api/subscriptions/',$http, $cookies, temp);
    }
    $scope.postCompare = function(exp,act){
        return false
      };

    // FILES upload controll :
    $scope.files = [];


    $scope.addPFilter = function(data) {
        $scope.filterGeoData = new Array();
        for( var item in data ){
            $scope.filterGeoData.push(data[item].id);
        };
    };

    $scope.geoFilter = function(item) {

        if($scope.filterGeoData == undefined || $scope.filterGeoData.length == 0)
            return true;
        else {
            if($scope.filterGeoData.indexOf(item.id)!=-1){
                return true;
            }else {
                return false;
            }
        }
    };


    $rootScope.$on('upload:loadstart', function () {
        console.log('Controller: on `loadstart`');
    });

    $rootScope.$on('upload:error', function () {
        console.log('Controller: on `error`');
    });

    $rootScope.$on('upload:success', function(xhr){

    });
  }]);

function sendCSRFPost(url,$http,$cookies,data){
    var thisdata = data;
    $http.defaults.headers.post['X-CSRFToken'] = $cookies['csrftoken'];
    $http.post(url, data).
        success(function (data, status, headers, config) {
                thisdata = data;
            }).
        error(function (data, status, headers, config) {
                console.log('Error ' +url+ '  ' + status);
            });
}

function sendRateToServer($http,$cookies,data){
    var thisdata = data;
    $http.defaults.headers.post['X-CSRFToken'] = $cookies['csrftoken'];
    $http.post('/zr/api/rates/',data).
        success(function (data, status, headers, config) {
                thisdata = data;
            }).
        error(function (data, status, headers, config) {
                console.log('Error ' + status);
            });
}
function sendTempToServer(data,$http,$cookies,callback){
    var thisdata = data;
    $http.defaults.headers.post['X-CSRFToken'] = $cookies['csrftoken'];
    $http.post('/zr/api/posts/',data).
        success(function (data, status, headers, config) {
                callback(data);
                thisdata = data;
            }).
        error(function (data, status, headers, config) {
                console.log('Error ' + status);
            });
}
var userLogedOn = function(user){
    if(user == "AnonymousUser"){
        return false;
    }
    return true;
}
var jsonToNestedCollection = function(jsonCollection, callback){
    jsonCollection.$promise.then(function(j){
        var all = {};
        var roots = [];
        for(var x in j){
            j[x].nodes = [];
            j[x].numcom = 0;
            all[j[x].id] = j[x];
        }
        for(var i in all){
            var obj = all[i];

            if( obj.parent == null)
                roots.push(obj);
            else {
                all[obj.parent].nodes.push(obj);
                all[obj.parent].numcom++;
            }
        }
    callback(roots);
    });
}

function parseWKTbeta(value) {
        var wkt = new Wkt.Wkt();
        wkt.read(value);
        var components = wkt.components[0];
        var bounds
        if (Array.isArray(components)){
            var latlngs = new Array();
            for (var i in components){
                var xy = components[i];
                var latlng = L.latLng(xy.y, xy.x);
                latlngs.push(L.latLng(xy.y, xy.x));
            }
            bounds = new L.LatLngBounds(latlngs);
        } else{
            var xy = components;
            var latlng = L.latLng(xy.y, xy.x);
            bounds = new L.LatLngBounds([latlng]);
        }
        return bounds
    }
