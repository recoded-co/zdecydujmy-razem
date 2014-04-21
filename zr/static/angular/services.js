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
        geometries_content: $resource('/zr/api/geometries/:id_param/?:para', {id_param:'@id'}, {
            get: {method:'GET', params:{para:'format=json'}, isArray:false}
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

phonecatServices.factory('postFactory', ['$resource',
  function($resource){
    return {
        newPostAll: $resource('/zr/api/npost/', {type:'date',round:'1',format:'json',parent:'None', direction:'False', geometry: 'None', plan_id:'None'}, {
          })
        /*,
        newPostFallow: $resource('/zr/api/npost/', {type:'date',round:'1',format:'json',parent:'None', direction:'True'}, {
          })*/
    }}]);


//'configurations','rates','subjects','posts','geometries','plans',

// Factory
// -------
phonecatServices.factory('uploadService', ['$rootScope','$cookies', function ($rootScope,$cookies) {

    return {
        send: function (file,post_id,callback) {
            var data = new FormData(),
                xhr = new XMLHttpRequest();

            xhr.onloadstart = function () {
                $rootScope.$emit('upload:loadstart', xhr);
            };

            // When the request has failed.
            xhr.onerror = function (e) {
                $rootScope.$emit('upload:error', e);
            };

            // Send to server, where we can then access it with $_FILES['file].
            data.append('datafile', file, file.name);
            data.append('post_id',post_id)

            xhr.open('POST', '/zr/fmen/angular_post');
            xhr.setRequestHeader("X-CSRFToken",
                                 $cookies['csrftoken']);
            xhr.onreadystatechange = function() {
                if (xhr.readyState === 4) {
                    if (xhr.status === 200) {
                               callback(xhr.response);
                    } else {
                               console.log('file upload failure!');
                    }
            }
};
            xhr.send(data);

        }
    };
}]);
