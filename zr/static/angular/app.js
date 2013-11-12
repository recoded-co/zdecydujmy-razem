'use strict';
/* App Module */

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