/**
 * Created by marcinra on 1/18/14.
 */
(function(){
    angular.module('angularytics').factory('AngularyticsDataBaseHandler', function($log,$http,$cookies) {
        var service = {};

        service.trackPageView = function(url) {
            $log.log("URL visited", url);
        }

        service.trackEvent = function(category, action, opt_label, opt_value, opt_noninteraction) {
            sendCSRFPost('/zr/api/track/',$http,$cookies,
                {category:category,
                action:action,
                opt_label:opt_label,
                opt_value:opt_value,
                opt_noninteraction:opt_noninteraction});
        }

        return service;
    });
})();

function sendCSRFPost(url,$http,$cookies,data){
    var thisdata = data;
    $http.defaults.headers.post['X-CSRFToken'] = $cookies['csrftoken'];
    $http.post(url, data).
        success(function (data, status, headers, config) {
                thisdata = data;
            }).
        error(function (data, status, headers, config) {
                $log.log('Error ' +url+ '  ' + status);
            });
}