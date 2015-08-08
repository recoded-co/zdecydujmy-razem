'use strict';

/* Controllers */

var zdControllers = angular.module('zdControllers', ['ngCookies']);
//'configurations','rates','subjects','posts','geometries','plans',


zdControllers.controller('apiList',
    ['$scope',
    '$http',
    '$cookies',
    '$rootScope',
    'zdServicesFactory',
    'uploadService',
    'Angularytics',
    'postFactory',
    'pulsePointBuf',
    'Analytics',
    function($scope,
             $http,
             $cookies,
             $rootScope,
             zdServicesFactory,
             uploadService,
             Angularytics,
             postFactory,
             pulsePointBuf,
             Analytics
    ) {



    Angularytics.trackPageView = function(url) {
        $scope.url = url;
    }

    function postState(){
        return {
            round:1,
            reachEnd:false
        }
    }

    var postHandler = function(servHandler,nestH,plan_id){
        var servHandler = servHandler;
        var nestedHandler = nestH;
        var type = 'date';
        var direction = 'True';
        var brPostState = {'None': postState() }
        var geometry = 'None';
        var plan_id= plan_id;
        var text = '';
        return{
            setHandler: function(handler){
                postHandler = handler;
            },
            setSearchText: function(textp){
                text = textp;
            },
            setGeoParam: function(item){
                geometry = item;
            },
            cleanParams: function(){
                brPostState = {'None': postState() }
            },
            sortByDate: function(){
                type = 'date';
            },
            sortByNumComments: function(){
                type = 'com';
            },
            setDirection: function(temp){
                if(temp === true)
                    direction = "True";
                else
                    direction = "False";
            },
            // params: parent_id = number or 'None' if root level
            getPostList: function(parent_id, callback){
                var LIMIT=0;
                if( brPostState[parent_id] === undefined){
                    brPostState[parent_id] = postState();
                }
                var tempServHandler = undefined;

                // changing post service for nested comments,
                // nested comments are out of text or data search
                if(parent_id != 'None' && nestedHandler != undefined ){
                    //nested
                    LIMIT=0;
                    tempServHandler = nestedHandler;
                } else {
                    LIMIT=8
                    tempServHandler = servHandler;
                }
                tempServHandler.query({
                    text:text,
                    geometry: geometry,
                    type:type,
                    round:''+brPostState[parent_id].round,
                    format:'json',
                    plan_id:plan_id,
                    parent:parent_id,
                    direction:direction}).$promise.then( function (data){
                        if(!brPostState[parent_id].reachEnd)
                            callback(data);

                        if(data.length<LIMIT){
                            brPostState[parent_id].reachEnd = true;
                        } else {
                            brPostState[parent_id].round++;
                        }
                    });
            },
            getPostListParams: function(parent_id,paramList, callback){

                if( brPostState[parent_id] === undefined){
                    brPostState[parent_id] = postState();
                }
                var tempServHandler = undefined;

                // changing post service for nested comments,
                // nested comments are out of text or data search
                if(parent_id != 'None' && nestedHandler != undefined ){
                    //nested
                    tempServHandler = nestedHandler;
                } else {
                    //surface
                    tempServHandler = servHandler;
                }
                var params = {  round:''+brPostState[parent_id].round,
                                plan_id:plan_id};
                angular.extend(params,paramList);
                tempServHandler.query(params).$promise.then( function (data){
                        if(!brPostState[parent_id].reachEnd)
                            callback(data);

                        if(data.length<5){
                            brPostState[parent_id].reachEnd = true;
                        } else {
                            brPostState[parent_id].round++;
                        }
                    });
            },
            postReachEnd: function(parent_id){
                if(brPostState[parent_id] !== undefined)
                    return brPostState[parent_id].reachEnd;
                else
                    return true;
            }
        }
    }

    var tree = null;

    $scope.$watch('searchdate.date',function(x){
        if(x instanceof Object){

            tree = postHandler(postFactory.dateSearch,postFactory.newPostAll,configuration.getPlanId());
            //$scope.showallposts = true;
            var params = {
                year: x.getFullYear(),
                mon: x.getMonth()+1,
                day: x.getDate()
            }
            tree.getPostListParams('None', params, function(data){
                $scope.tree = data;
            });

            $scope.endTree = tree.postReachEnd('None');

            $scope.showallpoints = true;

            $scope.tracker('UWD', x);
        }
    });

    $scope.$watch('url', function() {
        if($scope.url=='/all'){
            tree = postHandler(postFactory.newPostAll,undefined,configuration.getPlanId());
            tree.setGeoParam('None');
            // Analytics.track('ZCA');
        } else if($scope.url=='/details'){
            tree = postHandler(postFactory.newPostAll,undefined,configuration.getPlanId());
            tree.setGeoParam('notNone');
            // Analytics.track('ZSZ');
        } else if($scope.url=='/subscriptions'){
            tree = postHandler(postFactory.newSubscribedPosts,undefined,configuration.getPlanId());
            // Analytics.track('ZSL');
        }
        tree.getPostList('None',function(data){
               $scope.tree = data;
        });
        $scope.pointPulseRm();
        $scope.endTree = tree.postReachEnd('None');
    });
    tree = postHandler(postFactory.newPostAll,undefined,configuration.getPlanId());
    tree.setGeoParam('notNone');

    $scope.addMorePosts = function(post,root) {
        if(post.parent == null){
            $scope.addNextPostsToRoot();
        }else{
            tree.getPostList(post.parent,function(data){
                root.nodes = root.nodes.concat(data);
            });
            post.endTree = tree.postReachEnd(post.parent);
        }
    };
    $scope.addNextPostsToRoot = function(){
            tree.getPostList('None',function(data){
                $scope.tree = $scope.tree.concat(data);
            });
            $scope.endTree = tree.postReachEnd('None');
        }
    $scope.setDateSorting = function(temp){
        tree.cleanParams();
        tree.sortByDate();
        tree.setDirection(temp);
        tree.getPostList('None',function(data){
            $scope.tree = data;
            $scope.tracker('USD', temp == true ? 'ASC' : 'DESC');
        });
        $scope.endTree = tree.postReachEnd('None');
    };
    $scope.setCommentsSorting = function(temp){
        tree.cleanParams();
        tree.sortByNumComments();
        tree.setDirection(temp);
        tree.getPostList('None',function(data){
            $scope.tree = data;
            $scope.tracker('USK', temp == true ? 'ASC' : 'DESC');
        });
        $scope.endTree = tree.postReachEnd('None');
    };

    $scope.showOneDown = function(data){
        if(data.rozwin==undefined || data.rozwin==false){
            data.rozwin=true;
            if(data.nodes === undefined){
                tree.getPostList(data.id,function(post_list){
                    data.nodes = []
                    data.nodes = data.nodes.concat(post_list);
                    });
            } else if(data.nodes.length < 5){
                tree.getPostList(data.id,function(post_list){
                    data.nodes = []
                    data.nodes = data.nodes.concat(post_list);
                });
            }
        } else {
            data.rozwin=false;
        }
    };

    $scope.predicate='date';
    $scope.reverse=true;
    $scope.data_arrow=true;
    $scope.showallpoints=false;

    var post_buff_id = 0;
    $scope.zoom_chase = function(post){
        if(post.parent==null && post_buff_id!=post.id){
            post_buff_id = post.id;
            zdServicesFactory.geometries_content.get({id_param:post.geometry}).$promise.then(function(data){
                map.fitBounds(parseWKTbeta(data.geoelement));

                $scope.pointPulseRm();
                $scope.pointPulseAdd(window.mapObjects[post.id]._icon.classList);
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
        data.negative_rate = data.negative_rate + 1;
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
                temp['userAdded']=true;
                data.nodes.unshift(temp);
                data.numcom++;
                $scope.track('UDOA', data.id);
            });
            data.text = "";
            data.zmiennac=false ;
            $scope.showOneDown(data);
    };


    $scope.showAll = function(){
        $scope.showallpoints = true ;
        $scope.filterGeoData=[];
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
        data.rozwin = true;
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
                temp['userAdded']=true;
                $scope.tree.unshift(temp);
            });
    };
    $scope.subscribe = function(data, subscribed){
        var temp = {
            post: data.id,
            user: parseInt(configuration.getAuthor()),
            active: !subscribed // TODO add variable which says what to do, activate | deactivate
        }
        sendCSRFPost('/zr/api/subscriptions/',$http, $cookies, temp);

        if (!subscribed)
            $scope.tracker('UFSA', data.id);
        else
            $scope.tracker('UFSD', data.id);
    };

    $scope.openModal = function(post) {
        $('#post-delete-modal').modal('show');

        $scope.current_post = post;
    };
    $scope.deletePost = function() {
        if (typeof $scope.current_post != 'undefined') {
            sendCSRFPost('/zr/api/posts/remove/', $http, $cookies, {id: $scope.current_post.id});
            $scope.tracker('MI', $scope.current_post.id);
        }

        $('#post-delete-modal').modal('hide');
    };

    $scope.postCompare = function(exp,act){
        return false
    };

    // FILES upload controll :
    $scope.files = [];


    $scope.addPFilter = function(data) {

        $scope.filterGeoData = new Array();
        if(data!==undefined){
            $scope.showallpoints = true;

            if(data && data.length == 1){
               tree = postHandler(postFactory.newPostAll,undefined,configuration.getPlanId());
               tree.setGeoParam(''+data[0].geometry);
               tree.cleanParams();
               tree.getPostList('None',function(data){
                    $scope.tree = data;
               });
               $scope.endTree = tree.postReachEnd('None');
            } else if(data && data.length > 1){
               tree = postHandler(postFactory.newPostAll,undefined,configuration.getPlanId());
               var geo_params = '';
               for(var item in data){
                   if(item==0){
                   }else{
                       geo_params +=',';
                   }

                   geo_params +=''+data[item].geometry;
               }
               tree.setGeoParam(''+geo_params);
               tree.cleanParams();
               tree.getPostList('None',function(data){
                    $scope.tree = data;
               });
               $scope.endTree = tree.postReachEnd('None');

            }

        }else{

            $scope.pointPulseRm();
            tree = postHandler(postFactory.newPostAll,undefined,configuration.getPlanId());
            tree.setGeoParam('notNone');
            $scope.showallpoints = false;

            tree.getPostList('None',function(data){
                   $scope.tree = data;
            });
            $scope.endTree = tree.postReachEnd('None');
        }
    };

    $scope.search = function(text){
        $scope.tracker('UST', text);

        if(text && text.length>=1){
            tree = postHandler(postFactory.textSearch,postFactory.newPostAll,configuration.getPlanId());
            tree.setGeoParam('notNone');

            tree.setSearchText(text);

            tree.getPostList('None',function(data){
                $scope.tree = data;
            });

            $scope.endTree = tree.postReachEnd('None');

            $scope.showallpoints = true;
        }
    }

    $rootScope.$on('upload:loadstart', function () {
        console.log('Controller: on `loadstart`');
    });

    $rootScope.$on('upload:error', function () {
        console.log('Controller: on `error`');
    });

    $rootScope.$on('upload:success', function(xhr){

    });

    $scope.showDiscussion = function() {
        $scope.pointPulseRm();
        tree = postHandler(postFactory.newPostAll,undefined,configuration.getPlanId());
        tree.setGeoParam('notNone');
        $scope.showallpoints = false;

        $scope.tracker('PCD');

        tree.getPostList('None',function(data){
            $scope.tree = data;
        });
        $scope.endTree = tree.postReachEnd('None');
    }

    $scope.tracker = function(action, obj) {
        Analytics.track(action, obj);
    }

    $scope.trackEvent = function(category, action, opt_label, opt_value, opt_noninteraction){
        Angularytics.trackEvent(category, action, opt_label, opt_value, opt_noninteraction);
    }

    $scope.pointPulseAdd = function(temp){
        pulsePointBuf.add(temp);
    }

    $scope.pointPulseRm = function(){
        pulsePointBuf.remove();
    }

  }])

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
