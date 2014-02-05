'use strict';

/* Filters */

angular.module('phonecatFilters', []).filter('checkmark', function() {
  return function(input) {
    return input ? '\u2713' : '\u2718';
  };
});

angular.module('searchFilters', []).filter('searchdate', function() {
  return function(inputA, inputB) {
    if (!angular.isUndefined(inputA) && !angular.isUndefined(inputB) && inputB.date != "") {
        var tempClients = [];
        angular.forEach(inputA,function(entry){
            var date = getDate(entry.date);
            if(inputB.date.valueOf()==date.valueOf()){
                tempClients.push(entry);
            }
        });
        return tempClients;
    } else {
        return inputA;
    }
  };
});

angular.module('dateTools', []).filter('fromToday', function() {
  return function(inputA) {
    if (!angular.isUndefined(inputA)) {
        var then = getDate(inputA), // month is zero based
            now  = new Date;               // no arguments -> current date
        var diff = Math.round((now - then) / (1000 * 60 * 60 * 24));
        if(diff==0){
            return 'dziś';
        } else if(diff==1){
            return '1 dzień';
        } else {
            return diff+" dni";
        }
    } else {
        return 'brak daty';
    }
  };
});

function getDate(text){
    var temp = text.split('-');
    var date = new Date(0);
    date.setYear(parseInt(temp[0]));
    date.setMonth(parseInt(temp[1])-1);
    date.setDate(parseInt(temp[2]));
    date.setHours(0);
    date.setMinutes(0);
    date.setSeconds(0);
    date.setMilliseconds(0);
    return date;
}