define(['../app'],function (app) {
  'use strict';
  app.config(
    ['$stateProvider','$urlRouterProvider',
      function($stateProvider, $urlRouterProvider){
        $urlRouterProvider
        .otherwise('/schedules');
        $stateProvider
        .state('schedules',{
          abstract : true,
          url : '/schedules',
          templateUrl : '/static/partials/schedules.html'
        })
        .state('schedules.ui',{
          url : '?subjects&busy&active',
          views: {
            'subjects@schedules': {
              templateUrl: '/static/partials/subjects.html'
            },
            'detail@schedules': {
              templateUrl: '/static/partials/schedules.detail.html'
            },
            'list@schedules': {
              templateUrl: '/static/partials/schedules.list.html'
            }
          }
        })
        .state('about',{
          url : '/about',
          templateUrl: '/static/partials/about.html'
        }) ;
      }]
  );
  app.value('$anchorScroll', angular.noop);
});
