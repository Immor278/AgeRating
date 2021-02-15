var gplay = require('google-play-scraper');
// var path = "C:\\Age_Rating\\App_downloader\\Downloads\\App_list\\";

var category = process.argv[2];
var collection = process.argv[3];
var num = process.argv[4];
var path = process.argv[5] + "App_list\\"

gplay.list({
  category: category,
  collection: gplay.collection[collection],
  num: num,
  fullDetail: true
})
.then((result)=>{
  fs = require('fs');
  if(!fs.existsSync(path)){
    fs.mkdirSync(path);
  }
  fs.writeFile(path + 'list_' + category + '_' + collection + '_' + num + '.json', JSON.stringify(result), function (err) {
    if (err) return console.log(err);
    console.log('list_' + category + '_' + collection + '_' + num + ' is generated.');
  });
});

// for (let key in gplay.category){
//   gplay.list({
//     category: key,
//     collection: gplay.collection.TOP_FREE,
//     num: 2000
//   })
//   .then((result)=>{
//       fs = require('fs');
//       fs.writeFile('results/results_' + key + '.txt', JSON.stringify(result), function (err) {
//         if (err) return console.log(err);
//         console.log(key + 'done');
//       });
//   });
// }