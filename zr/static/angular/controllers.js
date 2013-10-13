'use strict';

/* Controllers */

var zdControllers = angular.module('zdControllers', ['ngCookies']);
//'configurations','rates','subjects','posts','geometries','plans',

zdControllers.controller('apiList', ['$scope','$http','$cookies', 'zdServicesFactory',
  function($scope,$http,$cookies,zdServicesFactory ) {
    //$scope.configurations = zdServicesFactory.configurations.json();
    //$scope.rates = zdServicesFactory.rates.json();
    //$scope.geometries = zdServicesFactory.geometries.json();
    $scope.plans = zdServicesFactory.plans.json();
    //$scope.subjects = zdServicesFactory.subjects.json();
    jsonToNestedCollection(zdServicesFactory.posts.json(),function(data){
        $scope.tree = data;
        window.data = data;
    });
    $scope.showallposts = true;

    $scope.scoreUp = function(data){
        data.score = data.score + 1;
        var temp = {
            post: data.id,
            user: configuration.getAuthor(),
            like: true,
            rate: 1
        }
        sendCSRFPost('/zr/api/rates/',$http,$cookies,temp);
    }
    $scope.scoreDown = function(data){
        console.log('ddddddddddd');
        data.score = data.score - 1;
        var temp = {
            post: data.id,
            user: configuration.getAuthor(),
            like: false,
            rate: 1
        }
        sendCSRFPost('/zr/api/rates/',$http,$cookies,temp);
      }

    $scope.delete = function(data) {
        data.nodes = [];
        data.text = "";
        data.zmiennac=false;
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
                nodes: [],
                zmiennac:false
            }
            sendTempToServer(temp,$http,$cookies);
            data.nodes.unshift(temp);
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
            nodes: [],
            zmiennac:false
        }
        sendTempToServer(temp,$http,$cookies);
        data.nodes.push(temp);
        data.text = "";
        data.zmiennac=false;
    };
    //$scope.tree = zdServicesFactory.posts.json();

    $scope.comment = function(data){
        if(userLogedOn($scope.user)){
            data.zmiennac = true;
        }
    }
  }]);

function sendCSRFPost(url,$http,$cookies,data){
    var thisdata = data;
    $http.defaults.headers.post['X-CSRFToken'] = $cookies['csrftoken'];
    $http.post(url,data).
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
function sendTempToServer(data,$http,$cookies){
    var thisdata = data;
    $http.defaults.headers.post['X-CSRFToken'] = $cookies['csrftoken'];
    $http.post('/zr/api/posts/',data).
        success(function (data, status, headers, config) {
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
            all[j[x].id] = j[x];
        }
        for(var i in all){
            var obj = all[i];

            if( obj.parent == null)
                roots.push(obj);
            else
                all[obj.parent].nodes.push(obj);
        }
    callback(roots);
    });
}

//'configurations','rates','subjects','posts','geometries','plans',

