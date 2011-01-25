-- sql script to convert char based row path values to int based ones
alter table spot5_catalogue add column jnum integer;
alter table spot5_catalogue add column knum integer;
update spot5_catalogue set jnum=cast(j as integer);
update spot5_catalogue set knum=cast(k as integer);
alter table spot5_catalogue drop column j;
alter table spot5_catalogue drop column k;
alter table spot5_catalogue rename column jnum to j;
alter table spot5_catalogue rename column knum to k;

