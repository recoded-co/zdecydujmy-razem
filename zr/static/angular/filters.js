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
        var then = getFullDate(inputA), // month is zero based
            now  = new Date;
        var days = Math.round((now - then) / (1000 * 60 * 60 * 24)),
            hrest = Math.round((now - then) % (1000 * 60 * 60 * 24)),
            mrest = Math.round((now - then) % (1000 * 60 * 60));
        var hours = Math.floor(hrest / (1000 * 60 * 60));
        var minutes = Math.floor(mrest / (1000 * 60 ));
        if(days<1){
            if(hours==0){
                return minutes+" minut temu";
            } else {
                return hours+" godzin temu";
            }
        } else if(days==1){
            return days+" dzień temu";
        } else {
            return days+" dni temu";
        }
    } else {
        return 'brak daty';
    }
  };
});

angular.module('geoFilter', []).filter('geoFilter', function() {
  return function(items,filterGeoData) {
      var tempList = new Array();
      if(filterGeoData == undefined || filterGeoData.length == 0){
          return items;
      } else {
          angular.forEach(items,function(item){
                if(filterGeoData.indexOf(item.id)!=-1){
                    tempList.push(item);
                }
          });
          return tempList;
      }
    };
});

function getDate(text){
    //2013-11-23T23:00:00Z
    var temp = text.split(/[-T:Z]/);
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

function getFullDate(text){
    var temp = text.split(/[-T:Z]/);
    var date = new Date(0);
    date.setYear(parseInt(temp[0]));
    date.setMonth(parseInt(temp[1])-1);
    date.setDate(parseInt(temp[2]));
    date.setHours(parseInt(temp[3]));
    date.setMinutes(parseInt(temp[4]));
    date.setSeconds(parseInt(temp[5]));
    date.setMilliseconds(0);
    return date;
}