(function(){
    angular.module('analytics', []).provider('Analytics', function() {
        this.$get = [
            '$http',
            '$cookies',
            function ($http, $cookies) {
                var service = {};

                service.init = function() {}

                service.track = function(action, obj) {
                    obj = obj || null;

                    sendCSRFPost('/zr/api/event/', $http, $cookies, {
                        action: action,
                        obj: obj
                    });
                }

                return service;
            }
        ];

        var sendCSRFPost = function(url, $http, $cookies, data){
            $http.defaults.headers.post['X-CSRFToken'] = $cookies['csrftoken'];
            $http.post(url, data);
        };

    }).filter('tracker', [
        'Analytics',
        function (Analytics) {
            return function (entry, action, obj) {
                Analytics.track(action, obj);
                return entry;
            };
        }
    ]);
})();
