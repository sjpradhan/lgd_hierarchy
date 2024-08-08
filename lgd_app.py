import requests
import pandas as pd
from PIL import Image
import streamlit as st
import warnings
from io import BytesIO
import plotly.graph_objects as go
warnings.filterwarnings('ignore')

def main():

    profile_icon = "https://raw.githubusercontent.com/sjpradhan/lgd_hierarchy/main/Data/img_1.png"

    # Fetch the image from URL
    response = requests.get(profile_icon)
    image = Image.open(BytesIO(response.content))

    st.set_page_config(page_title="LGD Search Hierarchy", page_icon=image)

    st.title(":rainbow[LGD Hierarchy Data & Area Unit Converter]🗺️")

    try:
        st.markdown(
            """
            <style>
            .spacer {
                margin-top: 10px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        # Add a spacer div to create space
        st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)
    except Exception as e:
        pass

# About States-------------------------------------------------------------------------------------------------|

    try:
        col1, col2, col3, col4 = st.columns(4)

        with col4:
            st.image(profile_icon)

    except Exception as e:
        pass
    # Conversion factors from each unit to square meters
    conversion_factors = {
        "Acre": 4046.86,
        "Hectare": 10000,
        "Bigha": 1337.8,
        "Square meter": 1,
        "Square feet": 0.092903,
        "Biswa": 125.42,
        "Guntha": 101.17,
        "Square yard": 0.836127,
        "Cent": 40.4686,
        "Ground": 222.967,
        "Biswani": 50.93,
        "Dhur": 16.929,
        "Kanal": 505.857,
        "Katha": 126.441,
        "Chatak": 33.528,
        "Ghumao": 24281.13,
        "Killa": 4046.86,
        "Ankanam": 2.323,
        "Decimal": 40.4686
    }

    # Function to convert from one unit to another
    def convert_area(value, from_unit, to_unit):
        value_in_sq_meters = value * conversion_factors[from_unit]
        return value_in_sq_meters / conversion_factors[to_unit]

    st.header(":rainbow[Area Unit Converter]")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(":orange[Choose Unit]🤔")
        from_unit = st.selectbox("From unit:", list(conversion_factors.keys()))
        to_unit = st.selectbox("To unit:", list(conversion_factors.keys()))
        value = st.number_input("Enter the area value:", min_value=0.0, format="%.2f", step=1.0)
        # Perform the conversion
        converted_value = convert_area(value, from_unit, to_unit)

    with col2:
        # Add a slider to adjust the input value dynamically
        slider_value = st.slider("Adjust the area value:", min_value=0.0, max_value=10.0, value=0.0, step=0.1)
        if slider_value > 0:
            slider_converted_value = convert_area(slider_value, from_unit, to_unit)
            st.write(f"{slider_value} {from_unit} is equal to {slider_converted_value:.6f} {to_unit}")

    # Enable real-time updates
    if st.button("Convert"):
        st.write(f"{value} {from_unit} is equal to {converted_value:.6f} {to_unit}")

    # Add a table to show multiple conversions at once if there is a valid input value
    if value > 0:
        st.subheader(":orange[Multiple Conversions📔]")
        conversion_results = {unit: convert_area(value, from_unit, unit) for unit in conversion_factors.keys()}
        conversion_df = pd.DataFrame.from_dict(conversion_results, orient='index', columns=['Converted Value'])
        conversion_df['Converted Value'] = conversion_df['Converted Value'].astype(str)
        conversion_df.reset_index(inplace=True)
        conversion_df.rename(columns={'index': 'Unit Type'}, inplace=True)
        st.table(conversion_df)

    st.header(":rainbow[Local Directory Data (LGD)]")
    st.subheader(":orange[KPI⚡]")
    st.divider()

    try:
        @st.cache_data
        def load_state_data():
            state_url = "https://media.githubusercontent.com/media/sjpradhan/lgd_hierarchy/main/Data/State%20Details.csv"
            state_df = pd.read_csv(state_url)
            state_df = state_df[["State LGD Code"]]
            return state_df
        state_df = load_state_data()

        @st.cache_data
        def load_district_data():
            district_url = "https://media.githubusercontent.com/media/sjpradhan/lgd_hierarchy/main/Data/District%20Details.csv"
            district_df = pd.read_csv(district_url)
            district_df = district_df[["District LGD Code"]]
            return district_df
        district_df = load_district_data()

        @st.cache_data
        def load_sub_district_data():
            sub_district_url = "https://media.githubusercontent.com/media/sjpradhan/lgd_hierarchy/main/Data/Sub-districts%20Details.csv"
            sub_district_df = pd.read_csv(sub_district_url)
            sub_district_df = sub_district_df[["Sub-District LGD Code"]]
            sub_district_df["Sub-District LGD Code"] = sub_district_df["Sub-District LGD Code"].astype(str)
            return sub_district_df
        sub_district_df = load_sub_district_data()

        @st.cache_data
        def load_village_data():
            village_url = "https://media.githubusercontent.com/media/sjpradhan/lgd_hierarchy/main/Data/Village%20Details.csv"
            village_df = pd.read_csv(village_url)
            village_df = village_df[["Village Code",]]
            village_df["Village Code"] = village_df["Village Code"].astype(str)
            return village_df
        village_df = load_village_data()

        col1, col2, col3,col4 = st.columns(4)

        with col1:
            unique_state = state_df["State LGD Code"].nunique()
            st.metric(label= "**States / Union Territories**", value = unique_state)

        with col2:
            unique_district = district_df["District LGD Code"].nunique()
            st.metric(label="**Districts**", value=unique_district)

        with col3:
            unique_sub_district = sub_district_df["Sub-District LGD Code"].nunique()
            st.metric(label="**Sub-Districts**", value=unique_sub_district)

        with col4:
            unique_villages = village_df["Village Code"].nunique()
            st.metric(label="**Villages**", value=unique_villages)
    except Exception as e:
        st.error(f"error occur in KPI,{e}")
        pass

    try:
        st.markdown(
            """
            <style>
            .spacer {
                margin-top: 10px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        # Add a spacer div to create space
        st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)
    except Exception as e:
        pass

    try:
        col1, col2, col3 = st.columns(3)
        with col1:
            # Create Search bar
            search_term = st.text_input(":blue[Search by :green[State]/:orange[Code:]]🔎", "")
    except Exception as e:
        pass

    try:
        @st.cache_data
        def load_state_data():
            state_url = "https://media.githubusercontent.com/media/sjpradhan/lgd_hierarchy/main/Data/State%20Details.csv"
            state_df = pd.read_csv(state_url)

            state_df = state_df[["State LGD Code", "State Name (In English)", "State Name (In Local language)", "State or UT",
            "Census2011 Code"]]

            return state_df

        state_df = load_state_data()


        # Filter based on State Name & it's LGD code
        if search_term:
            filtered_records = state_df[
                state_df['State Name (In English)'].str.contains(search_term, case=False) |
                state_df['State LGD Code'].astype(str).str.contains(search_term)
                ]

            # If there is invalid search it will show no matching found
            if not filtered_records.empty:
                st.write(":blue[Filtered results:]", filtered_records.shape)
                st.write(filtered_records)
            else:
                st.write(":red[Opps! No matching results found.]🤦‍♂️")

        # Preview of state data
        st.subheader(":orange[State Data Preview]🫣",divider='rainbow')
        ":green[Rows & Columns In States]➡️", state_df.shape
        st.write(state_df.head())
    except Exception as e:
        st.error(f"error in state data preview,{e}")
        pass

# About Districts ---------------------------------------------------------------------------------------------|
    try:
        col1, col2, col3 = st.columns(3)
        with col1:
            # Create Search bar
            search_term = st.text_input(":blue[Search by :green[District]/:orange[Code:]]🔎", "")
    except Exception as e:
        pass

    try:
        @st.cache_data
        def load_district_data():
            district_url = "https://media.githubusercontent.com/media/sjpradhan/lgd_hierarchy/main/Data/District%20Details.csv"
            district_df = pd.read_csv(district_url)

            district_df = district_df[
                ["District LGD Code", "District Name (In English)", "District Name (In Local language)",
                 "Hierarchy", "Short Name of District", "Census2011 Code", "Pesa Status"]]

            return district_df

        district_df = load_district_data()

        # Filter based on District Name & it's LGD code
        if search_term:
            filtered_records = district_df[
                district_df['District Name (In English)'].str.contains(search_term, case=False) |
                district_df['District LGD Code'].astype(str).str.contains(search_term) |
                district_df['Hierarchy'].str.contains(search_term, case=False)
                ]

            # If there is invalid search it will show no matching found
            if not filtered_records.empty:
                st.write(":blue[Filtered results:]",filtered_records.shape)
                st.write(filtered_records)
            else:
                st.write(":red[Opps! No matching results found.]🤦‍♂️")

        # Preview of district data
        st.subheader(":orange[District Data Preview]🫣",divider='rainbow')
        ":green[Rows & Columns In Districts]➡️", district_df.shape
        st.write(district_df.head())
    except Exception as e:
        st.error(f"error in district data,{e}")
        pass

# About Sub-Districts-------------------------------------------------------------------------------------------|
    try:
        @st.cache_data
        def load_sub_district_data():
            sub_district_url = "https://media.githubusercontent.com/media/sjpradhan/lgd_hierarchy/main/Data/Sub-districts%20Details.csv"
            sub_district_df = pd.read_csv(sub_district_url)

            sub_district_df = sub_district_df[["Sub-District LGD Code","Sub-District Name (In English)",
            "Sub-District Name (In Local language)","Hierarchy","Census2011 Code", "Pesa Status"]]

            sub_district_df["Sub-District LGD Code"] = sub_district_df["Sub-District LGD Code"].astype(str)
            sub_district_df["Census2011 Code"].fillna(0, inplace=True)
            sub_district_df["Census2011 Code"] = sub_district_df["Census2011 Code"].astype(int).astype(str)

            return sub_district_df

        sub_district_df = load_sub_district_data()

        col1, col2, col3 = st.columns(3)

        with col1:
            # Create Search bar
            search_term = st.text_input(":blue[Search by :green[Sub-District]/:orange[Code:]]🔎", "")

        # Filter based on Sub-District Name & it's LGD code
        if search_term:
            filtered_records = sub_district_df[
                sub_district_df['Sub-District Name (In English)'].str.contains(search_term, case=False) |
                sub_district_df['Sub-District LGD Code'].astype(str).str.contains(search_term) |
                sub_district_df['Hierarchy'].astype(str).str.contains(search_term, case=False)
                ]

            # If there is invalid search it will show no matching found
            if not filtered_records.empty:
                st.write(":blue[Filtered results:]",filtered_records.shape)
                st.write(filtered_records)
            else:
                st.write(":red[Opps! No matching results found.]🤦‍♂️")

        # Preview of sub-district data
        st.subheader(":orange[Sub-District Data Preview]🫣",divider = "rainbow")
        ":green[Rows & Columns In Sub-Districts➡️]", sub_district_df.shape
        st.write(sub_district_df.head())
    except Exception as e:
        st.error(f"error in sub-district data, {e}")
        pass


# About Villages----------------------------------------------------------------------------------------------|

    try:
        @st.cache_data
        def load_village_data():
            village_url = "https://media.githubusercontent.com/media/sjpradhan/lgd_hierarchy/main/Data/Village%20Details.csv"
            village_df = pd.read_csv(village_url)
            village_df = village_df[["State Code","State Name (In English)","District Code","District Name (In English)",
                        "Sub-District Code","Sub-District Name (In English)","Village Code","Village Version",
                        "Village Name (In English)","Village Name (In Local)","Village Status","Census 2011 Code"]]
            village_df["Village Code"] = village_df["Village Code"].astype(str)
            village_df["Census 2011 Code"].fillna(0, inplace=True)
            village_df["Sub-District Code"].fillna(0, inplace = True)
            village_df["Census 2011 Code"] = village_df["Census 2011 Code"].astype(int).astype(str)
            village_df["Sub-District Code"] = village_df["Sub-District Code"].astype(int).astype(str)

            return village_df
        village_df = load_village_data()

        col1, col2, col3 = st.columns(3)

        with col1:
            # Create Search bar
            search_term = st.text_input(":blue[Search by :green[Village]/:orange[Code:]]🔎", "")

        # Filter based on Sub-District Name & it's LGD code
        if search_term:
            filtered_records = village_df[
                village_df['Village Name (In English)'].str.contains(search_term, case=False) |
                village_df['Village Code'].astype(str).str.contains(search_term) |
                village_df['State Code'].astype(str).str.contains(search_term) |
                village_df['State Name (In English)'].str.contains(search_term, case=False) |
                village_df['District Code'].astype(str).str.contains(search_term) |
                village_df['District Name (In English)'].str.contains(search_term, case=False) |
                village_df['Sub-District Code'].astype(str).str.contains(search_term) |
                village_df['Sub-District Name (In English)'].str.contains(search_term, case=False)
                ]

            # If there is invalid search it will show no matching found
            if not filtered_records.empty:
                st.write(":blue[Filtered results:]",filtered_records.shape)
                st.write(filtered_records)
            else:
                st.write(":red[Opps! No matching results found.]🤦‍♂️")

        # Preview of sub-district data
        st.subheader(":orange[Villages Data Preview]🫣",divider="rainbow")
        ":green[Rows & Columns In Villages]", village_df.shape
        st.write(village_df.head())

    except Exception as e:
        st.error(f"error in village data,{e}")
        pass

    st.subheader(":orange[State Wise Records📈]", divider="rainbow")

    try:
        @st.cache_data
        def loading_district_data():
            district_url = "https://media.githubusercontent.com/media/sjpradhan/lgd_hierarchy/main/Data/District%20Details.csv"
            district_df = pd.read_csv(district_url)
            district_df["Hierarchy"] = district_df["Hierarchy"].str.replace(r"\(State\)", "").str.split("(").str.get(
                0).str.strip()
            districts_count = district_df["Hierarchy"].value_counts().reset_index()
            return districts_count
        districts_count = loading_district_data()

        @st.cache_data
        def loading_sub_district_data():
            sub_district_url = "https://media.githubusercontent.com/media/sjpradhan/lgd_hierarchy/main/Data/Sub-districts%20Details.csv"
            sub_district_df = pd.read_csv(sub_district_url)
            sub_district_df = sub_district_df[["Hierarchy"]]
            sub_district_df["Hierarchy"] = sub_district_df["Hierarchy"].str.replace(r"\(State\)", "").str.split("(").str.get(
                1).str.strip()
            sub_district_df["Hierarchy"] = sub_district_df["Hierarchy"].str.replace("District\) / ", "", regex=True)
            sub_district_count = sub_district_df["Hierarchy"].value_counts().reset_index()
            replacements = {
                "Bhabua)": "Bihar",
                "East Nimar)": "Madhya Pradesh",
                "West Nimar)": "Madhya Pradesh"
            }
            sub_district_count["Hierarchy"] = sub_district_count["Hierarchy"].replace(replacements)
            sub_district_count = sub_district_count.groupby("Hierarchy")["count"].sum().reset_index()
            return sub_district_count
        sub_district_count = loading_sub_district_data()

        @st.cache_data
        def loading_village_data():
            village_url = "https://media.githubusercontent.com/media/sjpradhan/lgd_hierarchy/main/Data/Village%20Details.csv"
            village_df = pd.read_csv(village_url)
            village_df = village_df[["State Name (In English)"]]
            village_count = village_df["State Name (In English)"].value_counts().reset_index()

            df_merge = pd.merge(districts_count, sub_district_count, how="left", on="Hierarchy")
            df_merge = pd.merge(df_merge, village_count, how="left", left_on="Hierarchy", right_on="State Name (In English)")
            stats_table = df_merge[["Hierarchy", "count_x", "count_y", "count"]]
            stats_table["count"].fillna(0, inplace=True)
            stats_table["count"] = stats_table["count"].astype(int)
            rename_column = ["States", "Districts", "Sub-Districts", "Villages"]
            stats_table.columns = rename_column
            return stats_table
        stats_table = loading_village_data()

        st.table(stats_table)
        st.caption("**Update till June 2024, To get latest LGD Data Please visit LGD Official site.**")
    except Exception as e:
        st.error(f"error in table data,{e}")
        pass

    st.divider()

    # col1,col2 = st.columns(2)

    # try:
    #     top_dist = stats_table[['States', 'Districts']].sort_values(by='Districts', ascending=False).head(5)
    #     # st.write(top_dist)
    #     fig = go.Figure(data=[go.Pie(labels=top_dist['States'], values=top_dist['Districts'], hole=0.5)])
    #     fig.update_layout(title='Top 10 States most Districts')
    #     fig.update_traces(hole=0.6)
    #     with col1:
    #         st.plotly_chart(fig)
    # except Exception as e:
    #     st.error(f"An error occurred: {e}")
    #     pass
    #
    # top_sub_dist = stats_table[['States', 'Sub-Districts']].sort_values(by='Sub-Districts', ascending=False).head(5)
    # fig = go.Figure(data=[go.Pie(labels=top_sub_dist['States'], values=top_sub_dist['Sub-Districts'], hole=0.5)])
    # fig.update_layout(annotations=[dict(text='Sub-Districts', x=0.5, y=0.5, font_size=16, showarrow=False)])
    #
    # with col2:
    #     st.plotly_chart(fig)
    #
    # top_villages = stats_table[['States', 'Villages']].sort_values(by='Villages', ascending=False).head(10)
    #
    # fig = go.Figure(data=[go.Bar(x=top_villages['States'], y=top_villages['Villages'])])
    # fig.update_layout(
    #     title='Top 10 States by most Villages',
    #     xaxis_title='States',
    #     yaxis_title='Number of Villages'
    # )
    # st.plotly_chart(fig)

# Footer
    st.markdown(
        """
        <style>
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #f4f4f4;
            padding: 10px 0;
            text-align: center;
        }
        </style>
        """
        , unsafe_allow_html=True
    )

    # Icons
    st.markdown(
        """
        <div class="footer" style="display: flex; justify-content: center; align-items: center;">
                <div style="display: inline-block;">
                    <a href="https://github.com/sjpradhan"><img src="https://raw.githubusercontent.com/sjpradhan/repo/master/Icons/github-logo.png" width="30" height="30"></a>
                    &nbsp;&nbsp;&nbsp;&nbsp;
                    <a href="mailto:sjpradan@gmail.com"><img src="https://raw.githubusercontent.com/sjpradhan/repo/master/Icons/gmail.png" width="30" height="30"></a>
                    &nbsp;&nbsp;&nbsp;&nbsp;
                    <a href="https://www.linkedin.com/in/sjpradhan"><img src="https://raw.githubusercontent.com/sjpradhan/repo/master/Icons/linkedin.png" width="30" height="30"></a>
                <div style="text-align: center;">
                    <p style="margin: 0;">© 2024 sj-lgd.</p>
                </div>
            </div>
        </div>
        """
        , unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()