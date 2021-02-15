var gplay = require('google-play-scraper');

var appID = process.argv[2];
// var folder = process.argv[3];
var num = process.argv[3];
var path = process.argv[4] + "Reviews\\"

// var path = "C:\\Age_Rating\\App_downloader\\Downloads\\Reviews\\";

gplay.reviews({
    appId: appID,
    sort: gplay.sort.RATING,
    num: num
  })
.then((result)=>{
  fs = require('fs');
  if(!fs.existsSync(path)){
    fs.mkdirSync(path);
  }
  fs.writeFile(path + 'review_' + appID + '.json', JSON.stringify(result), function (err) {
    if (err) return console.log(err);
    console.log('review_' + appID + ' is generated.');
  });
});