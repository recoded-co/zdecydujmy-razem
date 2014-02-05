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
  '$strap.directives',
  'angularytics',
  'ui.bootstrap.datetimepicker',
  'searchFilters',
  'dateTools'
]);

zdApp.config(function(AngularyticsProvider) {
    AngularyticsProvider.setEventHandlers(['Console','DataBase']);
  }).run(function(Angularytics) {
    Angularytics.init();
  });


zdApp.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});
