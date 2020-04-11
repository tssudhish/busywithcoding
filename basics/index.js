// Simple Hello World to main index html
console.log('Hello World');
// cannot be reserved keyword
// Should be meaningful
// variables cannot start with a number
// cannot contain space or hypen
const pi=355/113




let person={
    firstName:"Sudhish",
    lastName:"Kumar",
    age:39,
    selectedColor:['red','green','cyan'],
    isGood:true,

};

function greet(person) {
    console.log("From function call")
    console.log(person);

}

greet(person);