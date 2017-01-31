
SET SESSION query_cache_type = OFF;

EXPLAIN EXTENDED SELECT sum(l_extendedprice * l_discount) as revenue FROM lineitem WHERE l_shipdate >= date '1994-01-01' and l_shipdate < date '1994-01-01' + interval '1' year and l_discount between .06 - 0.01 and .06 + 0.01 and l_quantity < 24;
