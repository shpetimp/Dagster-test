{{ config(materialized='table') }}

select allinone.Product as Product_allinone, allinone_popup.Product as Product_allinone_popup,
allinone.Price as Price_allinone, allinone_popup.Price as Price_allinone_popup,
allinone.Description as Description_allinone, allinone_popup.Description as Description_allinone_popup,
allinone.Rating as Rating_allinone, allinone_popup.Rating as Rating_allinone_popup
from {{ source('allinone', 'allinone') }}
LEFT JOIN {{ source('allinone', 'allinone_popup') }} ON allinone.Product=allinone_popup.Product