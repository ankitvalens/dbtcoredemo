with
source as (
    select * from {{ ref('new') }}
),

newe as (

    select
        customer_id as customer_id,
        first_name,
        last_name

    from source

)

select * from newe