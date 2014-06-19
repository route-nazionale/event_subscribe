jQuery.event.props.push('dataTransfer');

//var EventSubscribeApp = angular.module('EventSubscribeApp', ['ngRoute', 'ngTable', 'lvl.directives.dragdrop']);
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
        $http.defaults.headers.post = {'X-CSRFToken': CSRF_TOKEN};
        $scope.events = [];
        $scope.order = 'name';
        $scope.alert = null;
        $scope.reverse = false;
        $scope.selectedEvent = null;
        $scope.subscribedEvents = [];
        $scope.slotEvents = {};
        $scope.tableParamsSlots = {};

        $scope.removeSlotEvent = function(slotId, slotEvent) {
            if (confirm('Vuoi davvero cancellare la tua iscrizione a ' + slotEvent.name + '?')) {
                $scope.slotEvents[slotId] = null;
                $scope.unsubscribe(slotEvent);
            }
        };
        $scope.getSlotEvent = function(slotId) {
            var e = $scope.slotEvents[slotId];
            return e;
        };
        $scope.findEvent = function(id) {
            for (var e in $scope.events) {
                var event = $scope.events[e];
                if (event.num === id) {
                    return event;
                }
            }
        };
        $scope.dropped = function(dragEl, dropEl) {
            var eid = $(dragEl).data('eventid');
            var sid = $(dropEl).data('slotid');
            var event = $scope.findEvent(eid);
            event.timeslot = sid;
            if (confirm('Vuoi davvero iscriverti a ' + event.name + '?')) {
                $scope.subscribe(event);
            }
        };
        $scope.showAlert = function(title, message) {
            $scope.alert = {title: title, message: message};
        };
        $scope.closeAlert = function() {
            $scope.alert = null;
        };
        $scope.selectEvent = function(event) {
            $scope.selectedEvent = event;
        };
        $scope.subscribedEvent = function(event) {
            var res = $scope.subscribedEvents.indexOf(event) >= 0;
            return res;
        };
        $scope.reload = function() {
            for (var s in $scope.tableParamsSlots) {
                $scope.tableParamsSlots[s].reload();
            }
        };
        $scope.subscribe = function(event) {
            var url = '/event/' + event.happening_id + '/subscribe/';
            $http.post(url).success(function(res) {
                if (res.status === 'OK') {
                    $scope.slotEvents[event.timeslot] = event;
                    $scope.subscribedEvents.push(event);
                } else {
                    $scope.showAlert(res.status, res.message);
                }
            });
        };
        $scope.unsubscribe = function(event) {
            var url = '/event/' + event.happening_id + '/unsubscribe/';
            $http.post(url).success(function(res) {
                if (res.status === 'OK') {
                    var id = $scope.subscribedEvents.indexOf(event);
                    if (id >= 0) {
                        $scope.subscribedEvents.splice(id, 1);
                    }
                } else {
                    $scope.showAlert(res.status, res.message);
                }
            });
        };
        $scope.getEventsForTimeslot = function(timeslot) {
            return $scope.events.filter(function(e) {
                return e.timeslot === timeslot;
            });
        };
        $scope.getEventById = function(happening_id) {
            for (var e in $scope.events) {
                if ($scope.events[e].happening_id === happening_id) {
                    return $scope.events[e];
                }
            }
            return null;
        };
        $scope.getTableParams = function(id) {
            return $scope.tableParamsSlots[id];
        };
        $scope.districtFilters = {};
        $scope.heartbeatFilters = {};
        $scope.handicapFilters = {};
        $scope.chiefonlyFilters = {};
        $scope.kindFilters = {};
        $scope.createTableParams = function(timeslot) {
            var params = new ngTableParams({
                page: 1, count: 25, 
                sorting: {name: 'asc'}
            }, {
                total: $scope.events.length,
                getData: function($defer, params) {
                    var data = $scope.getEventsForTimeslot(params.timeslot);
                    var filteredData = params.customFilter(data);
                    var orderedData = params.sorting() ?
                      $filter('orderBy')(filteredData, params.orderBy()) :
                      filteredData;
                    var start = (params.page() - 1) * params.count();
                    var stop = params.page() * params.count();
                    var range = orderedData.slice(start, stop);
                    params.total(range.length);
                    $defer.resolve(range);
                }
            });
            params.timeslot = timeslot;
            params.customFilter = function(data){
                var filtered = [];
                var districtFilter = $scope.districtFilters[timeslot];
                var heartbeatFilter = $scope.heartbeatFilters[timeslot];
                var handicapFitler = $scope.handicapFilters[timeslot];
                var chiefonlyFilter = $scope.chiefonlyFilters[timeslot];
                var kindFilter = $scope.kindFilters[timeslot];
                if( !districtFilter 
                    && !heartbeatFilter 
                    && !handicapFitler 
                    && !chiefonlyFilter 
                    && !kindFilter ){
                    return data;
                }
                for( var d in data ){
                    if( districtFilter ){
                        if( data[d].district.match(new RegExp(districtFilter)) ){
                            filtered.push(data[d]);
                            continue;
                        }
                    }
                    if( heartbeatFilter ){
                        if( data[d].heartbeat && data[d].heartbeat.match(new RegExp(heartbeatFilter)) ){
                            filtered.push(data[d]);
                            continue;
                        }
                    }
                    if( handicapFitler ){
                        if( data[d].state_handicap === 'ENABLED' ){
                            filtered.push(data[d]);
                            continue;
                        }
                    }
                    if( chiefonlyFilter ){
                        if( data[d].state_chief === 'RESERVED' ){
                            filtered.push(data[d]);
                            continue;
                        }
                    }
                    if( kindFilter ){
                        if( data[d].kind.match(new RegExp(kindFilter)) ){
                            filtered.push(data[d]);
                            continue;
                        }
                    }
                }
                return filtered;
            };
            return params;
        };

        $http.get('/events/').success(function(data) {
            $scope.events = data;

            for (var e in $scope.events) {
                var event = $scope.events[e];
                if (!(event.timeslot in $scope.slotEvents)) {
                    $scope.slotEvents[event.timeslot] = null;
                    $scope.districtFilters[event.timeslot] = '';
                    $scope.heartbeatFilters[event.timeslot] = '';
                    $scope.handicapFilters[event.timeslot] = '';
                    $scope.chiefonlyFilters[event.timeslot] = '';
                    $scope.tableParamsSlots[event.timeslot] = $scope.createTableParams(event.timeslot);
                }
            }

            $http.get('/myevents/').success(function(events) {
                for (var e in events) {
                    $scope.slotEvents[events[e].timeslot] = events[e];
                }
            });
        });
    }
]
  );
