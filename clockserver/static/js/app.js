'use strict';

angular.module('AlarmClock', [
  'ngResource',
  'AlarmClock.clock',
  'AlarmClock.weather'
]).config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
});
