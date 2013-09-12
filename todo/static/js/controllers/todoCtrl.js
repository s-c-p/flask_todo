/*global todomvc, angular */
'use strict';

/**
 * The main controller for the app. The controller:
 * - retrieves and persists the model via the todoStorage service
 * - exposes the model to the template and provides event handlers
 */
todomvc.controller('TodoCtrl', function TodoCtrl($scope, $http, $location, todoStorage, filterFilter) {
    $scope.logined = false;
    $scope.username = "";
    $scope.password = "";
    $scope.user_id;

    setloginCtrl($scope, $http);

    $scope.$watch('logined', function(){
        if ($scope.logined) {
            console.log('$scope.user_id : ' + $scope.user_id);
            getMemos($scope, $http, $location, todoStorage, filterFilter);
        }
    });
});

function getMemos($scope, $http, $location, todoStorage, filterFilter) {
    $http.get('/user/' + $scope.user_id + '/memos/').
        success(function(data, status) {
            set_todo_controller($scope, $http, $location, todoStorage, filterFilter, data);
        }).
        error(function(data, status) {
            console.log('edata : ' + data);
    });
}

function set_todo_controller($scope, $http, $location, todoStorage, filterFilter, memos) {
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
        $http.post('/user/' + $scope.user_id + '/memos/',  memo_data).
            success(function(data, status) {
                if (data['todo_memo_id'] !== 0) {
                    todos.splice(0, 0, {
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
            updataMemoData($scope, $http, todo);
        }
    };

    $scope.revertEditing = function (todo) {
        todos[todos.indexOf(todo)] = $scope.originalTodo;
        $scope.doneEditing($scope.originalTodo);
    };

    $scope.removeTodo = function (todo) {

        removeMemoData ($scope, $http, todos, todo);
    };

    $scope.clearCompletedTodos = function () {
        console.log('clearCompletedTodos')

        todos.forEach(function (todo) {
            if (todo.completed) {
                removeMemoData ($scope, $http, todos, todo);
            }
        });

        $scope.todos = todos = todos.filter(function (val) {
            return !val.completed;
        });
    };

    $scope.markAll = function (completed) {
        todos.forEach(function (todo) {
            todo.completed = completed;
            updataMemoData($scope, $http, todo);
        });
    };

    $scope.changeTodoStatus = function (todo) {
        updataMemoData($scope, $http, todo);
    };
}

function removeMemoData ($scope, $http, todos, todo) {
    $http.delete('/user/' + $scope.user_id + '/memos/' + todo.todo_memo_id).
        success(function(data, status) {

            if (data['status'] === 0) {
                todos.splice(todos.indexOf(todo), 1);
            }
        }).
        error(function(data, status) {
            console.log('edata : ' + data);
    });
}

function updataMemoData($scope, $http, todo) {
    var memo_data = 'memo=' + todo.title.trim() + '&state=' +
        (todo.completed ? 'complete' : 'incomplete');

    $http.defaults.headers.put["Content-Type"] = "application/x-www-form-urlencoded";
    $http.put('/user/' + $scope.user_id + '/memos/' + todo.todo_memo_id,  memo_data).
        success(function(data, status) {
            todo.title = todo.title.trim();
        }).
        error(function(data, status) {
            console.log('edata : ' + data);
    });
}

function setloginCtrl($scope, $http) {

    $scope.login = function() {
        if(this.username) {
            $scope.username = this.username;
            var login_data = 'username=' + this.username + '&password=' + this.password;

            $http.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded";
            $http.post('/login',  login_data).
                success(function(data, status) {

                    if (data['return_code'] === 0) {
                        console.log(data);
                        $scope.user_id = data['user_id'];
                        $scope.logined = true;
                    } else {
                        console.log(data);
                    }
                }).
                error(function(data, status) {
                    console.log('edata : ' + data);
            });
        }
    };

    $scope.logout = function() {
        $http.get('/logout').
            success(function(data, status) {
                $scope.logined = false;
                $scope.username = "";
                $scope.password = "";
            }).
            error(function(data, status) {
                console.log('edata : ' + data);
        });
    };
}
