'use strict';

angular.module('AlarmClock.clock', [
])

.controller('ClockDisplayCtrl', ['$scope', '$timeout',
  function ($scope, $timeout) {
    $scope.current_date = null;

    function refreshDate () {
      // Set $scope.date to now
      $scope.current_date = new Date();
      // Prepare next refresh
      $timeout(refreshDate, 1000);
    }

    // Start Clock
    refreshDate();

  }]);
