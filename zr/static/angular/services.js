'use strict';

/* Services */

var phonecatServices = angular.module('zdServices', ['ngResource']);

// "plans": "http://localhost:8000/zr/api/plans/",
phonecatServices.factory('zdServicesFactory', ['$resource',
  function($resource){
    return {
        plans: $resource('/zr/api/plans/?:para', {}, {
            json: {method:'GET', params:{para:'format=json'}, isArray:true}
          }),
        geometries: $resource('/zr/api/geometries/?:para', {}, {
            json: {method:'GET', params:{para:'format=json'}, isArray:true}
            }),
        posts: $resource('/zr/api/posts/?:para', {}, {
            json: {method:'GET', params:{para:'format=json'}, isArray:true}
            }),
        subjects:$resource('/zr/api/subjects/?:para', {}, {
            json: {method:'GET', params:{para:'format=json'}, isArray:true}
            }),
        rates:$resource('/zr/api/rates/?:para', {}, {
            json: {method:'GET', params:{para:'format=json'}, isArray:true}
            }),
       configurations: $resource('/zr/api/configurations/?:para', {}, {
            json: {method:'GET', params:{para:'format=json'}, isArray:true}
            })
      }
  }]);

 //'configurations','rates','subjects','posts','geometries','plans',

// Factory
// -------
phonecatServices.factory('uploadService', ['$rootScope','$cookies', function ($rootScope,$cookies) {

    return {
        send: function (file,post_id) {

            var data = new FormData(),
                xhr = new XMLHttpRequest();
            console.log(xhr);
            //$http.defaults.headers.post['X-CSRFToken'] = $cookies['csrftoken'];

            xhr.onloadstart = function () {
                console.log('Factory: upload started: ', file.name);
                $rootScope.$emit('upload:loadstart', xhr);
            };

            // When the request has failed.
            xhr.onerror = function (e) {
                $rootScope.$emit('upload:error', e);
            };

            // Send to server, where we can then access it with $_FILES['file].
            data.append('file', file, file.name);
            data.append('post_id',post_id)
            xhr.open('POST', '/zr/fmen/angular_post');
            xhr.send(data);
        }
    };
}]);
