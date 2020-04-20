//
//Java Script For Main Page
//
function onDropDownClick() {
    var dropDownMenu = document.getElementById("dropDownClick");
    console.log("Clicked on: " + dropDownMenu.className);
    if (dropDownMenu.className === "webnav") {
        dropDownMenu.className += " responsive";
    } else {
        dropDownMenu.className = "webnav";
    }
}


//---------------------------------------------------------------
//
//
//
//
//---------------------------------------------------------------
