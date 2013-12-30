'use strict';

/* Directives */

zdApp.directive('fileChange',['uploadService', function (uploadService) {

    var linker = function ($scope, element, attributes) {
        element.bind('change', function (event) {
            var files = event.target.files;
            for (var i = 0, length = files.length; i < length; i++) {
                if(files[i].size < 5242880)
                    uploadService.send(files[i],$scope.$parent.post.id, function(data){
                        var json_data = JSON.parse(data);
                        $scope.$parent.post.filep.push({name:json_data.name,
                            id:json_data.id,
                            file:json_data.file});
                        $scope.$apply();
                    });
                else{
                    alert('plik nie powinien przekraczać 5Mb');
                }
            }
        });
    };
    return {
        restrict: 'A',
        link: linker

    };
}]);

zdApp.directive('dropbox',['uploadService', function (uploadService) {

    var linker = function ($scope, element, attributes) {

        element[0].ondragover = function(evt) {
            evt.stopPropagation();
            evt.preventDefault();
            if( !element[0].classList.contains('filedragablearea'))
                element[0].classList.add('filedragablearea');

        };
        element[0].ondragleave = function(evt) {
            evt.stopPropagation();
            evt.preventDefault();
            if( element[0].classList.contains('filedragablearea'))
                element[0].classList.remove('filedragablearea');
        };

        element[0].ondrop = function (event) {
            event.stopPropagation();
            event.preventDefault();
            var files = event.dataTransfer.files;
            for (var i = 0, length = files.length; i < length; i++) {
                if(files[i].size < 5242880)
                    uploadService.send(files[i],$scope.$parent.post.id, function(data){
                        var json_data = JSON.parse(data);
                        $scope.$parent.post.filep.push({name:json_data.name,
                            id:json_data.id,
                            file:json_data.file});
                        $scope.$apply();
                    });
                else{
                    alert('plik nie powinien przekraczać 5Mb');
                }
            }
        };
    };
    return {
        restrict: 'C',
        link: linker

    };
}]);