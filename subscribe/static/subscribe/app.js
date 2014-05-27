
var EventSubscribeApp = angular.module('EventSubscribeApp', ['ngRoute', 'ngTable']);
EventSubscribeApp.config([
    '$routeProvider',
    function($routeProvider) {
        $routeProvider.
                when('/home', {
                    templateUrl: '/static/subscribe/partials/events.html',
                    controller: 'EventController'
                }).
                otherwise({
                    redirectTo: '/home'
                });
    }]);
EventSubscribeApp.controller('EventController', [
    '$scope', '$http', '$filter', 'ngTableParams',
    function($scope, $http, $filter, ngTableParams) {
        $scope.events = [];
        $scope.order = 'name';
        $scope.reverse = false;
        $scope.selectedEvent = {name:'????'};

        $scope.selectEvent = function(event){
            $scope.selectedEvent = event;
        };
        
        $http.get('/events/').success(function(data) {
            for( var e in data ){
                $scope.events.push(data[e].fields);
            }
            
            $scope.tableParams = new ngTableParams({
                page: 1, count: 10, sorting: { name: 'asc' }
            }, {
                total: $scope.events.length,
                getData: function($defer, params) {
                    var orderedData = params.sorting() ?
                            $filter('orderBy')($scope.events, params.orderBy()) :
                            $scope.events;
                    var start = (params.page() - 1) * params.count();
                    var stop = params.page() * params.count();
                    var range = orderedData.slice(start, stop);
                    $defer.resolve(range);
                }
            });

        });
    }
]
        );
