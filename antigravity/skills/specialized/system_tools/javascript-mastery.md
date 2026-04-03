---
name: "JavaScript Mastery"
tags: ["antigravity", "c:", "call", "concepts", "core", "gemini", "javascript", "<YOUR_USERNAME>", "mastery", "overview", "primitive", "reference", "specialized", "stack", "system", "tools", "types", "users", "value", "workflows"]
tier: 2
risk: "medium"
estimated_tokens: 2246
tools_needed: ["git", "markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["engineering", "productivity"]
quality_score: 0.95
---
# JavaScript Mastery

> **Tier:** 2-3  
> **Tags:** `javascript`, `js`, `concepts`, `fundamentals`, `advanced`  
> **When to Use:** Deep JavaScript understanding, interview prep, advanced patterns

---

## Overview

33+ essential JavaScript concepts every developer should know. From fundamentals to advanced patterns.

**Inspired by:** [33-js-concepts](https://github.com/leonardomso/33-js-concepts)

---

## Core Concepts

### 1. Call Stack
- Execution context stack
- LIFO (Last In, First Out)
- Stack overflow errors

### 2. Primitive Types
- `undefined`, `null`, `boolean`, `number`, `string`, `symbol`, `bigint`
- Immutable values
- Pass by value

### 3. Value Types vs Reference Types
```javascript
// Value (primitive)
let a = 5;
let b = a;  // Copy value
b = 10;     // a is still 5

// Reference (object)
let obj1 = { x: 5 };
let obj2 = obj1;  // Copy reference
obj2.x = 10;      // obj1.x is now 10
```

### 4. Type Coercion
```javascript
// Implicit coercion
"5" + 3      // "53" (string)
"5" - 3      // 2 (number)
true + 1     // 2
false + 1    // 1

// Explicit coercion
Number("5")  // 5
String(5)    // "5"
Boolean(0)   // false
```

### 5. == vs ===
```javascript
5 == "5"     // true (coercion)
5 === "5"    // false (strict)
null == undefined   // true
null === undefined  // false
```

### 6. Function Scope, Block Scope, Lexical Scope
```javascript
// Function scope (var)
function test() {
    var x = 1;
    if (true) {
        var x = 2;  // Same variable
    }
    console.log(x);  // 2
}

// Block scope (let/const)
function test() {
    let x = 1;
    if (true) {
        let x = 2;  // Different variable
    }
    console.log(x);  // 1
}

// Lexical scope
function outer() {
    const x = 1;
    function inner() {
        console.log(x);  // Access outer scope
    }
    inner();
}
```

### 7. Expression vs Statement
```javascript
// Expression (produces value)
5 + 3
x > 10
function() {}

// Statement (performs action)
if (x > 10) { }
for (let i = 0; i < 10; i++) { }
let x = 5;
```

### 8. IIFE (Immediately Invoked Function Expression)
```javascript
(function() {
    // Private scope
    const secret = "hidden";
})();

// Arrow function IIFE
(() => {
    console.log("Executed immediately");
})();
```

### 9. Hoisting
```javascript
// Variable hoisting
console.log(x);  // undefined (not error)
var x = 5;

// Function hoisting
foo();  // Works!
function foo() {
    console.log("Hello");
}

// let/const not hoisted
console.log(y);  // ReferenceError
let y = 5;
```

### 10. Closures
```javascript
function makeCounter() {
    let count = 0;
    return function() {
        return ++count;
    };
}

const counter = makeCounter();
console.log(counter());  // 1
console.log(counter());  // 2
```

### 11. Higher Order Functions
```javascript
// Function that takes/returns functions
function withLogging(fn) {
    return function(...args) {
        console.log("Calling with:", args);
        return fn(...args);
    };
}

const add = (a, b) => a + b;
const loggedAdd = withLogging(add);
loggedAdd(2, 3);  // Logs then returns 5
```

### 12. Recursion
```javascript
function factorial(n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

// Tail recursion (optimizable)
function factorialTail(n, acc = 1) {
    if (n <= 1) return acc;
    return factorialTail(n - 1, n * acc);
}
```

### 13. this Keyword
```javascript
// Global context
console.log(this);  // window (browser)

// Object method
const obj = {
    name: "Alice",
    greet() {
        console.log(this.name);  // "Alice"
    }
};

// Arrow function (lexical this)
const obj2 = {
    name: "Bob",
    greet: () => {
        console.log(this.name);  // undefined (inherits outer this)
    }
};

// Explicit binding
function greet() {
    console.log(this.name);
}
greet.call({ name: "Charlie" });  // "Charlie"
```

### 14. call, apply, bind
```javascript
function greet(greeting) {
    console.log(`${greeting}, ${this.name}`);
}

const person = { name: "Alice" };

// call (args individually)
greet.call(person, "Hello");

// apply (args as array)
greet.apply(person, ["Hi"]);

// bind (returns new function)
const boundGreet = greet.bind(person);
boundGreet("Hey");
```

### 15. Prototypes & Inheritance
```javascript
// Prototype chain
function Animal(name) {
    this.name = name;
}
Animal.prototype.speak = function() {
    console.log(`${this.name} makes a sound`);
};

function Dog(name) {
    Animal.call(this, name);
}
Dog.prototype = Object.create(Animal.prototype);
Dog.prototype.constructor = Dog;

const dog = new Dog("Rex");
dog.speak();  // "Rex makes a sound"
```

### 16. Object.create vs new
```javascript
// new keyword
function Person(name) {
    this.name = name;
}
const p1 = new Person("Alice");

// Object.create
const personProto = {
    greet() {
        console.log(`Hello, ${this.name}`);
    }
};
const p2 = Object.create(personProto);
p2.name = "Bob";
```

### 17. Classes (ES6)
```javascript
class Animal {
    constructor(name) {
        this.name = name;
    }
    
    speak() {
        console.log(`${this.name} makes a sound`);
    }
}

class Dog extends Animal {
    speak() {
        console.log(`${this.name} barks`);
    }
}

const dog = new Dog("Rex");
dog.speak();  // "Rex barks"
```

### 18. Promises
```javascript
const promise = new Promise((resolve, reject) => {
    setTimeout(() => {
        resolve("Success!");
    }, 1000);
});

promise
    .then(result => console.log(result))
    .catch(error => console.error(error))
    .finally(() => console.log("Done"));
```

### 19. async/await
```javascript
async function fetchData() {
    try {
        const response = await fetch(url);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Error:", error);
    }
}
```

### 20. Event Loop
```javascript
console.log("1");

setTimeout(() => {
    console.log("2");
}, 0);

Promise.resolve().then(() => {
    console.log("3");
});

console.log("4");

// Output: 1, 4, 3, 2
// Microtasks (Promises) before macrotasks (setTimeout)
```

---

## Advanced Concepts

### 21. Debounce & Throttle
```javascript
// Debounce: Wait until user stops typing
function debounce(fn, delay) {
    let timeoutId;
    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => fn(...args), delay);
    };
}

// Throttle: Execute at most once per interval
function throttle(fn, interval) {
    let lastTime = 0;
    return function(...args) {
        const now = Date.now();
        if (now - lastTime >= interval) {
            lastTime = now;
            fn(...args);
        }
    };
}
```

### 22. Currying
```javascript
function curry(fn) {
    return function curried(...args) {
        if (args.length >= fn.length) {
            return fn(...args);
        }
        return (...moreArgs) => curried(...args, ...moreArgs);
    };
}

const add = (a, b, c) => a + b + c;
const curriedAdd = curry(add);
curriedAdd(1)(2)(3);  // 6
curriedAdd(1, 2)(3);  // 6
```

### 23. Memoization
```javascript
function memoize(fn) {
    const cache = new Map();
    return function(...args) {
        const key = JSON.stringify(args);
        if (cache.has(key)) {
            return cache.get(key);
        }
        const result = fn(...args);
        cache.set(key, result);
        return result;
    };
}

const fibonacci = memoize(n => {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
});
```

### 24. Generators
```javascript
function* idGenerator() {
    let id = 1;
    while (true) {
        yield id++;
    }
}

const gen = idGenerator();
console.log(gen.next().value);  // 1
console.log(gen.next().value);  // 2
```

### 25. Proxy & Reflect
```javascript
const handler = {
    get(target, prop) {
        console.log(`Getting ${prop}`);
        return Reflect.get(target, prop);
    },
    set(target, prop, value) {
        console.log(`Setting ${prop} to ${value}`);
        return Reflect.set(target, prop, value);
    }
};

const obj = new Proxy({}, handler);
obj.name = "Alice";  // Logs: Setting name to Alice
console.log(obj.name);  // Logs: Getting name, then "Alice"
```

---

## Quick Reference

| Concept | Key Point |
|---------|-----------|
| Closures | Inner function accesses outer scope |
| Hoisting | var/function declarations moved to top |
| this | Context depends on how function is called |
| Promises | Async operations with then/catch |
| Event Loop | Microtasks before macrotasks |
| Prototypes | Inheritance via prototype chain |

---

## Related Skills

- `typescript-expert.md` - TypeScript patterns
- `react-patterns.md` - React with JavaScript
- `performance-hunter.md` - JS performance optimization

---

## Resources

- [33 JS Concepts](https://github.com/leonardomso/33-js-concepts)
- [MDN JavaScript Guide](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide)
- [JavaScript.info](https://javascript.info/)

---

**Version:** 1.0.0  
**Last Updated:** 2024-03-26  
**Size:** ~8KB
