# from web_scraper_project.allinone.web_scraper_allinone import allinone
# from web_scraper_project.allinone.web_scraper_allinone_popup import allinone_popup
from dagster import Definitions, load_assets_from_modules
from dagster._utils import file_relative_path
from dagster_dbt import dbt_cli_resource, load_assets_from_dbt_project
from web_scraper_project import assets
from web_scraper_project.assets import DBT_PROJECT_DIR, DBT_PROFILES_DIR


# DBT_PROJECT_DIR = file_relative_path(__file__, "../bigquery_scraper")
# DBT_PROFILES_DIR = file_relative_path(__file__, "../bigquery_scraper/config")

resources = {
    "dbt": dbt_cli_resource.configured(
        {"project_dir": DBT_PROJECT_DIR, "profiles_dir": DBT_PROFILES_DIR}
    )
}

defs = Definitions(assets=load_assets_from_modules([assets]), resources=resources)
# defs = Definitions(
#     assets=[*dbt_assets, allinone, allinone_popup],
#     resources=resources,
# )
