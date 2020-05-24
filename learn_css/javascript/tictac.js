var xSign;
var oSign;
var blankSign;
blankSign='&#8192';
oSign='&cir;';
xSign='&cross;';

var selectedSign=oSign;
var computerSign=xSign;

var gameBox =document.getElementById('gameBoxID');
var boxElems = document.getElementsByClassName('box');
var resetButton = document.getElementById('resetID');
var cancelButton = document.getElementById('cancelID');

//Add click event for any child class .box  of div = gamebox
var clicked_cell = $(document).ready(function(){
    $('.gamebox').on('mousedown', '.box', function(e){
        console.log(this.className);
        console.log(this.childNodes[1]);
        // BUG: hardcoding first index of object
        var currentSign=this.childNodes[1].innerHTML;
        if (currentSign.trim().length === 0) {
            this.childNodes[1].innerHTML=selectedSign;
        } else {
            console.log("Press an empty cell");
        }

        console.log("Selected cell:" + $(this).index());
    }).on('mouseup','.box',function() {
        checkWin();
    });
});

function getBoxElementValue(index) {
    return gameBox.children[index].children[0].innerHTML;
}


// check boxes for win
function checkBoxes(index1,index2,index3) {
    var val1=getBoxElementValue(index1);
    var val2=getBoxElementValue(index2);
    var val3=getBoxElementValue(index3);
    
    if(val1 === val2 && 
       val2 === val3 && 
       (val1.trim().length > 0 &&
        val2.trim().length > 0 &&
        val3.trim().length > 0
       ))
    {

        console.log(index1,index2,index3);
        console.log("val1 | val2 | val3");
        console.log(val1+" "+val2+" "+val3);
        return true;
    } else {
        return false;
    }
}

function checkWin() {
    var winStatus=false;
    var winType=undefined;
    var windowID=undefined;

    console.log("Check if game is over");

    if (checkBoxes(0,1,2)){
        // row-wise
        // 0-1-2
        winStatus=true;
        winType="row-1";
        windowID="winIDRow";

    } else if (checkBoxes(3,4,5)) {
        // 3-4-5
        winStatus=true;
        winType="row-2";
        windowID="winIDRow";

    } else if (checkBoxes(6,7,8)) {
        // 6-7-8
        winStatus=true;
        winType="row-3";
        windowID="winIDRow";

    } else if (checkBoxes(0,3,6)) {
        // column-wise
        // 0-3-6
        winStatus=true;
        winType="col-1";
        windowID="winIDCol";

    } else if (checkBoxes(1,4,7)) {
        // 1-4-7
        winStatus=true;
        winType="col-2";
        windowID="winIDCol";

    } else if (checkBoxes(2,5,8)) {
        // 2-5-8
        winStatus=true;
        winType="col-3";
        windowID="winIDCol";

    } else if (checkBoxes(0,4,8)) {
        // diagonally
        // 0-4-8
        winStatus=true;
        winType="diag-main";
        windowID="winIDMain";

    } else if (checkBoxes(2,4,6)) {
        // 2-4-6
        winStatus=true;
        winType="diag-alt";
        windowID="winIDAlt";

    } else {
        winStatus=false;
        winType=undefined;
        insertRandomElement();
    }
    console.log(winType);
    if (winType !== undefined) {
        var winbox = document.getElementById(windowID);
        winbox.style.zIndex="1";
        var winTypeElem = document.getElementById(winType);
        winTypeElem.style.visibility="visible";
    }
}

function getGridElementsPosition(index) {
    //Get the css attribute grid-template-columns from the css of class grid
    //split on whitespace and get the length, this will give you how many columns

    const colCount = $('.gamebox').css('grid-template-columns').split(' ').length;
    const rowPosition = Math.floor(index / colCount);
    const colPosition = index % colCount;
    //Return an object with properties row and column
    return { row: rowPosition, column: colPosition } ;
}

function resetButtonCallBack() {
    console.log("RESET Button pressed"); 
    console.log(boxElems.length);
    for (var index=0; index<boxElems.length;index++) {
        box=boxElems[index];
        console.log('Working on ->');
        box.children[0].innerHTML=blankSign;
    }

    var windowList=document.querySelectorAll('[id^="winID"]');
    for (var index=0; index<windowList.length;index++) {
        var winObj=windowList[index];
        winObj.style.zIndex="-1";


        for (var jIndex=0;jIndex<winObj.children.length; jIndex++){
            winObj.children[jIndex].style.visibility="hidden";
        }

    }
}

function cancelButtonCallBack() {
    console.log("CANCEL Button pressed"); 
}

//////////////////Setting Up Computer to play//////////////

function insertRandomElement() {
    console.log("Computer playing");
    var randomSelection=undefined;
    for (var icounter=0;icounter<gameBox.children.length;icounter++) {
        randomSelection=Math.floor(Math.random()*9);
        if (getBoxElementValue(randomSelection).trim().length === 0) {
            gameBox.children[randomSelection].children[0].innerHTML=computerSign;
            break;
        }
    }
}
