'use strict';

/* Directives */

zdApp.directive('fileChange',['uploadService', function (uploadService) {

    var linker = function ($scope, element, attributes) {
        // onChange, push the files to $scope.files.

        element.bind('change', function (event) {
            var files = event.target.files;

            for (var i = 0, length = files.length; i < length; i++) {
                // Hand file off to uploadService.
                console.log(files[i]);
                uploadService.send(files[i],attributes.value, function(data){
                    console.log("data");
                    console.log(data);
                });
            }

            $scope.$apply(function () {

            });
        });
    };

    return {
        restrict: 'A',
        link: linker

    };
}]);
