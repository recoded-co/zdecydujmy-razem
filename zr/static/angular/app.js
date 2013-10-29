'use strict';
/* App Module */

var appConfiguration = function() {
    var appPlanId='1';
    var appAuthor='1';
    return {
        //init: function(){
        //    this.appAuthor=;
        // },
        getAuthor: function() {
            return appAuthor;
        },
        setPlanId: function(temp){
            this.appPlanId = temp;
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