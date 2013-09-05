/*global todomvc, angular */
'use strict';

/**
 * The main controller for the app. The controller:
 * - retrieves and persists the model via the todoStorage service
 * - exposes the model to the template and provides event handlers
 */
todomvc.controller('TodoCtrl', function TodoCtrl($scope, $http, $location, todoStorage, filterFilter) {
    getMemos($scope, $http, $location, todoStorage, filterFilter);
});

function getMemos($scope, $http, $location, todoStorage, filterFilter) {
    $http.get('/user/1/memos/').
        success(function(data, status) {
            set_controller($scope, $http, $location, todoStorage, filterFilter, data);
        }).
        error(function(data, status) {
            console.log('edata : ' + data);
    });
}

function set_controller($scope, $http, $location, todoStorage, filterFilter, memos) {
    var todos = $scope.todos = [];

    for (var i = memos.length - 1; i >= 0; i--) {
        todos.push({
            todo_memo_id : memos[i]["id"],
            title: memos[i]["memo"],
            completed: memos[i]['state'] == 'incomplete' ? false : true
        });
    }

    $scope.newTodo = '';
    $scope.editedTodo = null;

    $scope.$watch('todos', function (newValue, oldValue) {
        $scope.remainingCount = filterFilter(todos, { completed: false }).length;
        $scope.completedCount = todos.length - $scope.remainingCount;
        $scope.allChecked = !$scope.remainingCount;
    }, true);

    if ($location.path() === '') {
        //$location.path('/');
    }

    $scope.location = $location;

    $scope.$watch('location.path()', function (path) {
        $scope.statusFilter = (path === '/active') ?
            { completed: false } : (path === '/completed') ?
            { completed: true } : null;
    });

    $scope.addTodo = function () {
        var newTodo = $scope.newTodo.trim();
        if (!newTodo.length) {
            return;
        }

        var memo_data = 'memo=' + newTodo;

        $http.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded";
        $http.post('/user/1/memos/',  memo_data).
            success(function(data, status) {
                if (data['todo_memo_id'] !== 0) {
                    todos.push({
                        todo_memo_id : data['todo_memo_id'],
                        title: newTodo,
                        completed: false
                    });
                }
            }).
            error(function(data, status) {
                console.log('edata : ' + data);
        });

        $scope.newTodo = '';
    };

    $scope.editTodo = function (todo) {
        $scope.editedTodo = todo;
        // Clone the original todo to restore it on demand.
        $scope.originalTodo = angular.extend({}, todo);
    };

    $scope.doneEditing = function (todo) {
        $scope.editedTodo = null;

        if (!todo.title.trim()) {
            todo.title = todo.title.trim();
            $scope.removeTodo(todo);

        } else {
            updataMemoData($http, todo);
        }
    };

    $scope.revertEditing = function (todo) {
        todos[todos.indexOf(todo)] = $scope.originalTodo;
        $scope.doneEditing($scope.originalTodo);
    };

    $scope.removeTodo = function (todo) {
        console.log('todo_memo_id : ' + todo.todo_memo_id)

        $http.delete('/user/1/memos/' + todo.todo_memo_id).
            success(function(data, status) {

                if (data['status'] === 0) {
                    todos.splice(todos.indexOf(todo), 1);
                }
            }).
            error(function(data, status) {
                console.log('edata : ' + data);
        });
    };

    $scope.clearCompletedTodos = function () {
        $scope.todos = todos = todos.filter(function (val) {
            return !val.completed;
        });
    };

    $scope.markAll = function (completed) {
        console.log('markAll :' + completed)
        todos.forEach(function (todo) {
            todo.completed = completed;
            updataMemoData($http, todo);
        });
    };

    $scope.changeTodoStatus = function (todo) {
        updataMemoData($http, todo);
    };
}

function updataMemoData($http, todo) {
    var memo_data = 'memo=' + todo.title.trim() + '&state=' +
        (todo.completed ? 'complete' : 'incomplete');

    $http.defaults.headers.put["Content-Type"] = "application/x-www-form-urlencoded";
    $http.put('/user/1/memos/' + todo.todo_memo_id,  memo_data).
        success(function(data, status) {
            todo.title = todo.title.trim();
        }).
        error(function(data, status) {
            console.log('edata : ' + data);
    });
}
