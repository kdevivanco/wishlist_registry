-- MySQL dump 10.13  Distrib 8.0.31, for macos12 (x86_64)
--
-- Host: localhost    Database: wishlist2
-- ------------------------------------------------------
-- Server version	8.0.22

--
-- Dumping data for table `participants`
--

LOCK TABLES `participants` WRITE;
/*!40000 ALTER TABLE `participants` DISABLE KEYS */;
INSERT INTO `participants` VALUES (1,4,'requested'),(1,8,'requested'),(1,10,'requested'),(1,11,'requested'),(1,12,'requested'),(2,1,'accepted'),(4,1,'accepted'),(4,9,'accepted'),(5,9,'accepted');
/*!40000 ALTER TABLE `participants` ENABLE KEYS */;
UNLOCK TABLES;


--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (8,'Chupon Bibs','Chupones de caucho natural','https://anukay.com/products/bibs','https://imageserve.babycenter.com/14/000/244/6VxBZXqPuRE9DFAJQe7yEvApscXyT6p1_med.jpg',62,'2023-01-04 22:39:30','2023-01-04 22:39:30',1,'Anukay'),(9,'Silla de comer','Emilias baby shower','https://www.clebastien.com/p/silla-stokke-modelo-steps/','https://www.clebastien.com/wp-content/uploads/2020/12/349701-1.jpg',2099,'2023-01-04 22:40:03','2023-01-04 22:40:03',1,'Stokke'),(10,'Play Station 5 ','PS5 Digital Edition - Latam','https://www.falabella.com.pe/falabella-pe/product/882344492/PS5-Digital-Edition-Latam/882344492?kid=shopp8fc&disp=1&gclid=Cj0KCQiAzeSdBhC4ARIsACj36uEY5xGR8DeGaikg1Hv8PYjJmqxJwM1pGrGroDuyHz2l3UJjQjr-NxkaAhCiEALw_wcB','https://falabella.scene7.com/is/image/FalabellaPE/882344492_1?wid=1500&hei=1500&qlt=70',3099,'2023-01-07 19:29:03','2023-01-07 19:29:03',2,'Falabella'),(11,'Audífonos bluetooth in ear ',' Digital Perú BS19C, micrófono incorporado, con radio y ranura microsd, rojo','https://www.coolbox.pe/handsfree-bluetooth-bs19c-con-radio-y-ranura-microsd-color-rojo-13016/p','https://coolboxpe.vtexassets.com/arquivos/ids/232836-1200-auto?v=638010086723770000&width=1200&height=auto&aspect=true',29,'2023-01-07 19:32:01','2023-01-07 19:32:01',2,'Coolbox'),(12,'Silla de comer para bebes','Na','https://www.clebastien.com/p/silla-stokke-modelo-steps/','https://www.clebastien.com/wp-content/uploads/2020/12/349701-1.jpg',2400,'2023-01-08 10:56:25','2023-01-08 10:56:25',1,'Stokke'),(13,'Cocina a gas Bosch','Cocina a gas','https://tottus.falabella.com.pe/tottus-pe/product/113346257/bosch-cocina-24-con-encendido-electrico-y-hierro-fundido---pro425ix-41158186/113346258?disp=1&gclid=CjwKCAiA8OmdBhAgEiwAShr40xREL43asr10-osnodyRM6fdRzzKEPKM6rM5tkSeS9mKr-HCV1OTgRoCtbAQAvD_BwE&kid=shopp6fc','https://e39a9f00db6c5bc097f9-75bc5dce1d64f93372e7c97ed35869cb.ssl.cf1.rackcdn.com/41158186_1-KzAIzWMR.jpg?wid=1500&hei=1500&qlt=70',1099,'2023-01-08 18:40:26','2023-01-08 18:40:26',4,'BOSCH FALABELLA'),(14,'Luces led de colores','para decorar el escritorio','https://www.coolbox.pe/tira-luz-radioshack-rgb-flexible-2607047/p?idsku=6806&gclid=CjwKCAiA8OmdBhAgEiwAShr400u26rFzKQEM7rhdxEL-j04aDK6q3I9pyhnwQr-uCdkxoAj5gZeyThoCZ7cQAvD_BwE','https://coolboxpe.vtexassets.com/arquivos/ids/194890-1200-auto?v=637734878581200000&width=1200&height=auto&aspect=true',50,'2023-01-08 19:08:51','2023-01-08 19:08:51',1,'Coolbox'),(15,'Revlon secadora y estilizador','Secadora','https://simple.ripley.com.pe/peine-secador-y-voluminizador-revlon-one-step-2019267197178p?color_80=negro&s=mdco&gclid=CjwKCAiA8OmdBhAgEiwAShr40zLgBOmnTuTdZWAAFk4LtPOlZRX10y5rwKSCH7I0D1jEC2OjEP2PSxoCUwUQAvD_BwE','https://home.ripley.com.pe/Attachment/WOP_5/2019267197178/2019267197178_2.jpg',229,'2023-01-08 19:09:57','2023-01-08 19:09:57',1,'Ripley'),(16,'Zapatillas urbanas ','zapatillas','https://www.falabella.com.pe/falabella-pe/product/18765495/Zapatillas-urbanas-Mujer-Campo-Veja-CP0502429/18765501?kid=shopp2fc&disp=1&gclid=CjwKCAiA8OmdBhAgEiwAShr403oP8I9DYT-cFDzrdSTFXn-NSra0-dHjP60G4RJL-9pNbdhb4JJaNBoC1DUQAvD_BwE','https://falabella.scene7.com/is/image/FalabellaPE/18765501_1?wid=1500&hei=1500&qlt=70',799,'2023-01-08 19:10:42','2023-01-08 19:10:42',1,'Veja');
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;


--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Kayla','De Vivanco','kdevivanco@gmail.com','$2b$12$DimxngpHnT2b3SX31qUkQObiwZhJV6zrpk4wo.Iawv2OHvc2iZ3yS','2023-01-04 20:15:54','2023-01-04 20:15:54','https://media.licdn.com/dms/image/D4E03AQE_vhjm8dYK1A/profile-displayphoto-shrink_800_800/0/1663868161990?e=1678320000&v=beta&t=f2_TPBRwBfaiatc56m19v72RF_GwsgBG7bO7A5fx1bw'),(2,'Stefano','Campodonico','stefanocs97@gmail.com','$2b$12$szjg4SA/7lhhlF75dxBTY.5pAGpbxrN/7aSfWToi2f6ef5Z92cZSu','2023-01-04 22:07:11','2023-01-04 22:07:11','https://expo-arteydiseno.pucp.edu.pe/2020/wp-content/uploads/2021/01/3291PiCa5-2.jpg'),(3,'Talia ','Briceno','talia@briceno.com','$2b$12$zWCDmI0V8h7wFOlPxS/1EeT5qZVp5ayuJm/ms2tjQGq/fBcCh4uYS','2023-01-05 19:35:03','2023-01-05 19:35:03',''),(4,'Pedro Miguel','Schiaffino','pedrom@schiaffino.com','$2b$12$DRANBsV1U6VaJ7olvSKoAO.iIk1lV6UCa22kcXBO6/RvtOWmFcs.2','2023-01-08 18:37:39','2023-01-08 18:37:39','https://peru21.pe/resizer/PYXEQd5IrB_R1SA4tiBVAkeQILs=/580x330/smart/filters:format(jpeg):quality(75)/arc-anglerfish-arc2-prod-elcomercio.s3.amazonaws.com/public/N3W7F7ICHRDSFBX5VK5CEIJH3Q.jpg'),(5,'Sienna','Schiaffino','sienna@schiaffino.com','$2b$12$vwSUinphf15akRT6mDZjyeyyTV2DkAmrbYZOFlSKxSE7Qn4.Mzsoe','2023-01-08 19:13:57','2023-01-08 19:13:57','');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `wishlist_products`
--

LOCK TABLES `wishlist_products` WRITE;
/*!40000 ALTER TABLE `wishlist_products` DISABLE KEYS */;
INSERT INTO `wishlist_products` VALUES (8,2,10,6,'bought'),(8,2,11,7,'available'),(1,1,12,8,'bought'),(1,1,10,9,'available'),(9,1,11,10,'bought'),(9,1,11,11,'bought'),(11,4,13,12,'available'),(9,1,16,15,'available'),(9,1,13,16,'available'),(9,1,10,17,'available');
/*!40000 ALTER TABLE `wishlist_products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `wishlists`
--

LOCK TABLES `wishlists` WRITE;
/*!40000 ALTER TABLE `wishlists` DISABLE KEYS */;
INSERT INTO `wishlists` VALUES (1,'bebe Shower ','Emilias baby shower','Hi friends! This is my wishlist for Emilias Baby Shower. ','public','2023-01-04 20:21:52','2023-12-12 00:00:00',1,'https://imageserve.babycenter.com/14/000/244/6VxBZXqPuRE9DFAJQe7yEvApscXyT6p1_med.jpg'),(4,'Wedding Registry','My wedding Registry','Hi friends!','private','2023-01-05 19:36:41','2023-12-12 00:00:00',3,'https://blueflames.co.uk/wp-content/uploads/2021/09/wedding.png'),(8,'My birthday','My bd list','Hi friends, this is my wishlist for my bd. Feel free to pick whichever gift from here :)','private','2023-01-07 19:20:39','2023-10-02 00:00:00',2,'https://www.thoughtco.com/thmb/5Gst37ATS_ls1GBOQ2IXW3YGgbM=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/birthday-cake-with-candles-and-sparklers--529391959-5c25a2cb46e0fb0001c3dc44.jpg'),(9,'2023 wishlist','Things i wish to buy this year','This is private','private','2023-01-08 12:00:09','2023-12-12 00:00:00',1,'https://img.freepik.com/vector-gratis/logotipo-ano-2023-fuegos-artificiales-ilustracion-vectorial-fondo-azul_8130-1117.jpg?w=1480&t=st=1673197199~exp=1673197799~hmac=2f943bdedf3620b4b1a79f2a179573f5547b2e77de319258879344991f438c85'),(10,'Mi viaje a la nieve','Me voy de viaje a la nieve','Hola! Me gusta viajar','private','2023-01-08 18:30:41','2023-12-12 00:00:00',2,'https://upload.wikimedia.org/wikipedia/commons/thumb/1/16/Snowboarding.jpg/500px-Snowboarding.jpg'),(11,'Mi wishlist de cocina','Articulos de cocina que quiero comprar','Este es mi wishlist de cocina','private','2023-01-08 18:39:41','2024-01-12 00:00:00',4,'https://www.elmueble.com/medio/2021/03/27/cocina-blanca-con-grifo-y-lamparas-en-negro-00527512-o_2d710425_1600x2000.jpg'),(12,'Mi viaje a la playa','snfjsdbkjfdnbjd','dfbndfkjbfnjfd','private','2023-01-08 20:08:25','2024-12-12 00:00:00',5,'https://dictionary.cambridge.org/es/images/thumb/baby_noun_002_02163.jpg?version=5.0.286');
/*!40000 ALTER TABLE `wishlists` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;



/* AGREGANDO MIS PROPIOS DUMPS... */

INSERT INTO users ( first_name ,last_name, email , password , created_at, updated_at,profile_url ) 
VALUES ( 'Brisa' , 'de Vivanco' , 'brisadev@gmail.com' , '$2b$12$5jlYet7Jw5W1vmm0Fgsc7e0fkcgjEKn8dexi3lQU71e3Hf7DWw/5W' , NOW() , NOW(), '');


INSERT INTO users ( first_name ,last_name, email , password , created_at, updated_at,profile_url ) 
VALUES ( 'Annia' , 'de Vivanco' , 'annia@dev.com' , '$2b$12$K0NlmISXAgpIY3X1G8vGPeIkXimnvO2jAM7Nho.RqNEOr.hf9Fl7K' , NOW() , NOW(), '');

INSERT INTO wishlists ( name , description, text, privacy, img_url, created_at, end_date, creator_id) 
VALUES ( 'Mi cumpleaños' , 'Es mi cumpleaños en 10 dias!' ,'Hola amigos! Los invito a participar de mi wishlist cumpleañero', 'private', 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/MA_Route_23.svg/1200px-MA_Route_23.svg.png', NOW() , '2023-01-18', '7');

INSERT INTO products ( product_name , description,brand,link,price,img_url,creator_id, created_at, updated_at ) 
VALUES ( 'Vestido Rojo' , 'Este es el vestido que quiero para mi santo','FINA',  'https://finaperu.pe/products/vestido-diosa-jul-rojo?variant=42754779938947&currency=PEN&utm_medium=product_sync&utm_source=google&utm_content=sag_organic&utm_campaign=sag_organic&gclid=CjwKCAiA8OmdBhAgEiwAShr40yWfN5pCgPQBmYoqYqq8sPkX_6flHfN_MOv81gP3OJDHfYV8GdON7RoCqpUQAvD_BwE', '174', 'https://cdn.shopify.com/s/files/1/0392/8830/7843/products/vestido-diosa-jul-rojo-P23FIVS003ROJ-0007_1728x.jpg?v=1658525155', 7, NOW() , NOW());

INSERT INTO participants ( participant_id , wishlist_id, status ) 
VALUES ( 7 , '11', "requested");

INSERT INTO wishlist_products ( wishlist_id,wcreator_id,product_id,status) 
VALUES ( '13' , 7, '14', 'available');

INSERT INTO participant_purchases ( wishlist_id,product_id,participant_id) 
VALUES ( '13' , '14', '7');

INSERT INTO participants ( participant_id , wishlist_id, status ) 
                VALUES ( 1 , '13', "requested");


INSERT INTO users ( first_name ,last_name, email , password , created_at, updated_at,profile_url ) 
                VALUES ( 'Cristobal' , 'Campodonico' , 'cristobal@campodonico.com' , '$2b$12$XUpOfpsXcKZwGIjoc.S9Au6bszWITGZygk6GvZbtLjJi2asCDcUXy' , NOW() , NOW(), '');


INSERT INTO participants ( participant_id , wishlist_id, status ) 
                VALUES ( 8 , '1', "requested");

UPDATE participants
                SET status = 'accepted'
                WHERE participant_id = '8' and wishlist_id = '1';

