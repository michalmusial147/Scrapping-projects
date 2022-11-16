const canvasId = "myCanvas"
const filePath = "Łódź.csv"
const yOffset = 60;
let xMin = 0;
let xMax = 0;
let yMin = 0;
let yMax = 0;
const rectangles = []
const sectors = []

for(let i = 0 ; i< 4 ; i++) {
    for(let j = 0 ; j< 4 ; j++) {
        rectangles.push([i * 150, 450 - j * 150 + yOffset, 150, 150]);
        sectors.push([i * 150, 450 - j * 150, i * 150 + 150, 450 - j * 150 + 150, 0]);
    }
}

function norm(val, max, min) {
 return ((val - min) / (max - min) * 597);
}
function norm_y(val, max, min) {
 return 600 - ((val - min) / (max - min) * 597);
}
function drawPoint(ctx, x, y) {
     ctx.fillRect(norm(x, xMax, xMin), norm_y(y,  yMax, yMin) + yOffset, 5 , 5);
}

function loadFile(filePath) {
  var result = null;
  var xmlhttp = new XMLHttpRequest();
  xmlhttp.open("GET", filePath, false);
  xmlhttp.send();
  if (xmlhttp.status == 200) {
    result = xmlhttp.responseText;
  }
  return result;
}

const drawArea = (ctx) => {
    rectangles.forEach((element, i) => {
       ctx.strokeRect(...element)
       ctx.strokeText(i, element[0] + 75, element[1] + 76);
    });
}

function isInRectangle(x1, y1, x2, y2, x, y) {
    if (x > x1 && x < x2 && y > y1 && y < y2)
        return true;
    return false;
}
function findSector(x, y) {
    sectors.forEach((element, i) => {
       if(isInRectangle(
       element[0],
       element[1],
       element[2],
       element[3],
       norm(x, xMax, xMin),
       norm_y(y,  yMax, yMin)))
         {
            console.log(x + " / " + y + " found sector=" + i);
            element[4]+=1;
       }
    })
}

function drawCanvas(file_contents, canvasId){

  file_contents =  file_contents.split(/\r\n|\n/);
  const cityName = file_contents[0];
  const count = file_contents[1];
  const uselessHeader = file_contents[2];
  const cords = file_contents[3].split(",");
  xMin = cords[0];
  xMax = cords[1];
  yMin = cords[2];
  yMax = cords[3];
  const canvas = document.getElementById(canvasId);
  const ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  drawArea(ctx);
  ctx.font = "32px Arial";
  ctx.strokeText(cityName, 0, 25);
  ctx.font = "12px Arial";
  ctx.strokeText((xMin + "/"+ yMin), 0, 587 + yOffset);
  ctx.strokeText((xMax + "/"+ yMax), 550, 0  + yOffset);
  ctx.fillStyle = "#FF00FF";
  drawPoint(ctx, xMin, yMin);
  drawPoint(ctx, xMax, yMax);
  ctx.fillStyle = "#FF0000";
  const rows = file_contents.slice(5);
  rows.forEach(row => {
       const point_row = row.split(",")[1];
       if(point_row) {
         const point = point_row.split("/");
         if(point) {
             drawPoint(ctx, point[1], point[0]);
             findSector(point[1], point[0]);
         }
       }
    });
}

//drawCanvas(filePath, canvasId);

document.getElementById('inputfile')
.addEventListener('change', function() {

var fr=new FileReader();
fr.onload=function(){
    drawCanvas(fr.result, 'myCanvas');
}

fr.readAsText(this.files[0]);
})
