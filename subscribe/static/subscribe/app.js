jQuery.event.props.push('dataTransfer');

var EventSubscribeApp = angular.module('EventSubscribeApp', ['ngRoute', 'ngTable','lvl.directives.dragdrop']);
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
        $http.defaults.headers.post = { 'X-CSRFToken' : CSRF_TOKEN };
        $scope.events = [];
        $scope.order = 'name';
        $scope.alert = null;
        $scope.reverse = false;
        $scope.selectedEvent = null;
        $scope.subscribedEvents = [];
        $scope.slotEvents = {s0:null,s1:null,s2:null};
        $scope.tableParamsSlots = {};

        $scope.removeSlotEvent = function(slotId, slotEvent){
            if( confirm('Vuoi davvero cancellare la tua iscrizione a '+slotEvent.name+'?')){
                $scope.slotEvents[slotId] = null;
                $scope.unsubscribe(slotEvent);
            }
        };
        $scope.getSlotEvent = function(slotId){
            var e = $scope.slotEvents[slotId];
            return e;
        };
        $scope.findEvent = function(id){
            for(var e in $scope.events){
                var event = $scope.events[e];
                if( event.num === id ){
                    return event;
                }
            }
        };
        $scope.dropped = function(dragEl, dropEl) {
            var eid = $(dragEl).data('eventid');
            var sid = $(dropEl).data('slotid');
            var event = $scope.findEvent(eid);
            if( confirm('Vuoi davvero iscriverti a '+event.name+'?')){
                $scope.slotEvents[sid] = event;
                $scope.subscribe(event);
            }
        };
        $scope.showAlert = function(title,message){
            $scope.alert = {title:title, message:message};
        };
        $scope.closeAlert = function(){
            $scope.alert = null;
        };
        $scope.selectEvent = function(event){
            $scope.selectedEvent = event;
        };
        $scope.subscribedEvent = function(event){
            var res = $scope.subscribedEvents.indexOf(event) >= 0;
            return res;
        };
        $scope.reload = function(){
            for( var s in $scope.tableParamsSlots ){
                $scope.tableParamsSlots[s].reload();
            }
        };
        $scope.subscribe = function(event){
            var url = '/event/'+event.code+'/subscribe/';
            $http.post(url).success(function(res){
                if( res.status === 'OK' ){
                    $scope.subscribedEvents.push(event);
                }else{
                    $scope.showAlert(res.status,res.message);
                }
            });
        };
        $scope.unsubscribe = function(event){
            var url = '/event/'+event.code+'/unsubscribe/';
            $http.post(url).success(function(res){
                if( res.status === 'OK' ){
                    var id = $scope.subscribedEvents.indexOf(event);
                    if( id>=0 ){
                        $scope.subscribedEvents.splice(id,1);
                    }
                }else{
                    $scope.showAlert(res.status,res.message);
                }
            });
        };
        $scope.getTableParams = function(id){
            return $scope.tableParamsSlots[id];
        };
        
        $http.get('/events/').success(function(data) {
            $scope.events = data;
            
            for( var s in $scope.slotEvents ){
                $scope.tableParamsSlots[s] = new ngTableParams({
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
            }

        });
    }
]
        );
