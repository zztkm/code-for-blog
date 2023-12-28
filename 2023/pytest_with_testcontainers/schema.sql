create table `menus` (
  `id` int not null auto_increment,
  `code` varchar(255) not null,
  `name` varchar(255) not null,
  `price` int not null,
  `description` varchar(255) not null,
  primary key (`id`),
  unique key `menus_code_unique` (`code`)
) engine=InnoDB default charset=utf8mb4;
