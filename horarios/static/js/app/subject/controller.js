/**
* Subject controller definition
* @scope Controllers
*/
define(['./module'], function (controllers) {
  'use strict';
  controllers.controller('SubjectCtrl', function ($scope,SubjectService,ScheduleService,ngProgress, $state, $rootScope) {
    /*
     * lists all the currently selected subjects
     */
    $scope.subjects = SubjectService.get();
    /*
     * emits an event to rootScope when subjects are changed
     */
    $scope.$watchCollection('subjects', function() {
      $scope.changeGroup();
    });
    /*
     * loads the autocomplete service
     */
    $scope.autocomplete = function(name){
      return SubjectService.autoComplete(name);
    };
    /*
     * adds a selected subject to the subjects list
     */
    $scope.onSelect = function ($item) {
      SubjectService.add($item).then(function(added){
        if(added){
          ScheduleService.setSubjectQuery(SubjectService.getQuery());
          $rootScope.$broadcast('ScheduleParamsChange');
          ngProgress.start();
        }
      });
    };
    /*
     * removes a subject from the selected subjects
     */
    $scope.removeSubject = function(code){
      SubjectService.del(code);
      ScheduleService.setSubjectQuery(SubjectService.getQuery());
      $rootScope.$broadcast('ScheduleParamsChange');
    };
    /*
     * changes the check status for the given children
     */
    $scope.checkChange = function(items,value, isChild){
      items.forEach(function(item){
        item.isChecked = value;
        if(item.hasOwnProperty('groups')){
          $scope.checkChange(item.groups,value,true);
        }
      });
      if ( isChild === undefined ) {
        $scope.changeGroup();
      }
    };
    /*
     * toggles the group and emits the scheduleChange event
     */
    var emit = function() {
      ScheduleService.setSubjectQuery(SubjectService.getQuery());
      $scope.$emit('scheduleChange');
      if(ngProgress.status() === 0){
      } else if(ngProgress.status() < 50){
        ngProgress.set(50);
      }

    };
    /*
     * Formats the input on the typeahead
     */
    $scope.formatInput = function(){
      return '';
    };
    /*
     * checks every 5 seconds for changes if a change is detected it fires
     * a subject change event
     */
    $scope.changeGroup = function(){
      $rootScope.$broadcast('ScheduleParamsChange');
      //var throttledEmit = _.throttle(emit, 1500, { 'leading': false, 'trailing': true });
      //throttledEmit();
    };
    $scope.$on('SubjectsAdded', function(){

    });
  });
});
