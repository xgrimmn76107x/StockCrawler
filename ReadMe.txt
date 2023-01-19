每次缺資料的時候，就到stock.csv存在的資料夾執行: 
docker run -v ${PWD}:/docker_stock_crawler demo_stock_crawler:v1


docker pull grimmn76107/demo_stock_crawler