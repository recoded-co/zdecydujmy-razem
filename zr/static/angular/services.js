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