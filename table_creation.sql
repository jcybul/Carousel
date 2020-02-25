#
create table Carousel
(
    Barrel_num   int         null,
    Date_planted date        null,
    Water_ec     double      null,
    Seed_type    varchar(30) null,
    Water_Liters double      null,
    constraint Carousel_Barrel_num_uindex
        unique (Barrel_num),
    check (`Water_ec` = 2.3 or `Water_ec` = 0)
);

create table Plant_records
(
    barrel_num    int          not null,
    date_recorded datetime     not null,
    Height        double       null,
    Comments      varchar(200) null,
    primary key (barrel_num, date_recorded)
);

