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
    '$scope', '$http', '$filter', '$timeout', 'ngTableParams',
    function($scope, $http, $filter, $timeout, ngTableParams) {
        $http.defaults.headers.post = {'X-CSRFToken': CSRF_TOKEN};
        $scope.events = [];
        $scope.order = 'name';
        $scope.alert = null;
        $scope.reverse = false;
        $scope.selectedEvent = null;
        $scope.subscribedEvents = [];
        $scope.slotEvents = {};
        $scope.timeslots = [];
        $scope.tableParamsSlots = {};
        $scope.heartbeats = [];
        $scope.districts = [];

        $scope.removeSlotEvent = function(slotId, slotEvent) {
            if (confirm('Vuoi davvero cancellare la tua iscrizione a ' + slotEvent.name + '?')) {
                $scope.slotEvents[slotId] = null;
                $scope.unsubscribe(slotEvent);
            }
        };
        $scope.getTimeslotById = function(id){
            for(var v in $scope.timeslots){
                if( $scope.timeslots[v].timeslot === id ){
                    return $scope.timeslots[v];
                }
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
                $scope.tableParamsSlots[s].page(1);
                $scope.tableParamsSlots[s].reload();
            }
        };
        $scope.subscribe = function(event) {
            if( event.seats_n_chiefs >= event.max_chiefs_seats ){
                alert('Non è più possibile iscriversi a questo evento.\nI posti sono esauriti.');
                return;
            }
            var url = '/event/' + event.happening_id + '/subscribe/';
            $http.post(url).success(function(res) {
                if (res.status === 'OK') {
                    $scope.slotEvents[event.timeslot] = event;
                    $scope.getTimeslotById(event.timeslot).event = event;
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
                        $scope.getTimeslotById(event.timeslot).event = null;
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
        $scope.printcodeFilters = {};
        $scope.kindFilters = {};
        $scope.loaded = false;
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
                    params.total(orderedData.length);
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
                var printcodeFilter = $scope.printcodeFilters[timeslot];
                if( !districtFilter 
                    && !heartbeatFilter 
                    && !handicapFitler 
                    && !chiefonlyFilter 
                    && !printcodeFilter 
                    && !kindFilter ){
                    return data;
                }
                for( var d in data ){
                    if( districtFilter ){
                        if( !data[d].district.match(new RegExp(districtFilter,'i')) ){
                            continue;
                        }
                    }
                    if( printcodeFilter ){
                        if( !data[d].print_code || !data[d].print_code.match(new RegExp(printcodeFilter,'i')) ){
                            continue;
                        }
                    }
                    if( heartbeatFilter ){
                        if( !data[d].heartbeat || !data[d].heartbeat.match(new RegExp(heartbeatFilter,'i')) ){
                            continue;
                        }
                    }
                    if( handicapFitler ){
                        if( data[d].state_handicap !== 'ENABLED' ){
                            continue;
                        }
                    }
                    if( chiefonlyFilter ){
                        if( data[d].state_chief !== 'RESERVED' ){
                            continue;
                        }
                    }
                    if( kindFilter ){
                        if( !data[d].kind.match(new RegExp(kindFilter,'i')) ){
                            continue;
                        }
                    }
                    filtered.push(data[d]);
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
                    $scope.timeslots.push( { index: parseInt(event.dt_start), timeslot: event.timeslot, event: null } );
                    $scope.districtFilters[event.timeslot] = '';
                    $scope.heartbeatFilters[event.timeslot] = '';
                    $scope.handicapFilters[event.timeslot] = '';
                    $scope.chiefonlyFilters[event.timeslot] = '';
                    $scope.printcodeFilters[event.timeslot] = '';
                    $scope.tableParamsSlots[event.timeslot] = $scope.createTableParams(event.timeslot);
                }
                if( $scope.districts.indexOf(event.district)<0 ){
                    $scope.districts.push(event.district);
                }
                if( $scope.heartbeats.indexOf(event.heartbeat)<0 ){
                    $scope.heartbeats.push(event.heartbeat);
                }
            }
            
            $scope.timeslots.sort(function(a,b){
                return a.index - b.index;
            });

            $http.get('/myevents/').success(function(events) {
                for (var e in events) {
                    $scope.slotEvents[events[e].timeslot] = events[e];
                    $scope.subscribedEvents.push(events[e]);
                    $scope.getTimeslotById(events[e].timeslot).event = events[e];
                }
                $scope.loaded = true;
            });
        });
    }
]
  );
