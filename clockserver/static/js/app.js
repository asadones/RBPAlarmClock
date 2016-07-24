'use strict';

angular.module('AlarmClock', [
  'AlarmClock.clock'
]).config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
});
