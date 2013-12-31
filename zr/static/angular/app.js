'use strict';
/* App Module */

var appConfiguration = function() {
    var appPlanId='1';
    var appAuthor='1';

    return {
        setAuthor: function(authorId){
            appAuthor=authorId;
        },
        getAuthor: function() {
            return appAuthor;
        },
        setPlanId: function(temp){
            appPlanId = temp;
        },
        getPlanId: function(){
            return appPlanId;
        }
    }
}
var configuration = appConfiguration();

var zdApp = angular.module('zd', [
  'ngRoute',
  'zdControllers',
  'zdServices',
  '$strap.directives'
]);

zdApp.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});
