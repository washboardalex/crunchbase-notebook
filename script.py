import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv(
    "data/crunchbase.csv",
    parse_dates=["Founded Date"],
    converters={
        # "Industries": lambda x: x[0:].split(","),
        "Headquarters Location": lambda x: x[0:].split(",")[-1],
    },
)

# Extract year for easy grouping
df["Founded Year"] = df["Founded Date"].dt.year

# Rename columns for ease of use
df = df.rename(
    columns={
        "Last Funding Amount Currency (in USD)": "Last Funding (USD)",
        "Last Equity Funding Amount Currency (in USD)": "Last Equity Funding (USD)",
    }
)

# Sanitise "Industries" column
df["Industries"] = df["Industries"].fillna("")

df.info()

# See companies founded by year
# In all cases drop 2023 as year is unfinished
df_group_year = df.groupby("Founded Year")["Founded Year"].count().drop(labels=2023)

# See non-blockchain companies founded by year
df_no_blockchain = df[~df["Industries"].str.contains("Blockchain")]
no_blockchain_grouped = (
    df_no_blockchain.groupby("Founded Year")["Founded Year"].count().drop(labels=2023)
)

# # See specifically blockchain companies founded by year
df_blockchain = df[df["Industries"].str.contains("Blockchain")]
blockchain_grouped = (
    df_blockchain.groupby("Founded Year")["Founded Year"].count().drop(labels=2023)
)

# Plot

fig, ax = plt.subplots(figsize=(8, 6))

df_group_year.plot(kind="line", ax=ax, label="Total Metaverse Foundings")
blockchain_grouped.plot(kind="line", ax=ax, label="Blockchain Foundings")
no_blockchain_grouped.plot(kind="line", ax=ax, label="Non-Blockchain Foundings")

plt.legend()
plt.show()

# By region over time

# First get 10 largest regions for this

fig2, ax2 = plt.subplots(figsize=(8, 8))

reg_col = "Headquarters Location"

regions = df.groupby(reg_col)[reg_col].count()

main_regions = regions.nlargest(10, keep="first")


main_regions.plot(kind="bar", ax=ax2, label="Foundings By Region")

plt.show()

# Now we want to plot them all in a time series
plt.cla()
fig3, ax3 = plt.subplots(figsize=(9, 9))

for country in main_regions.keys():
    if country == "":
        continue;
    df_country = df[df[reg_col].str.contains(country)]
    df_country_grouped = (
        df_country.groupby("Founded Year")["Founded Year"].count().drop(2023, errors='ignore')
    )
    df_country_grouped.plot(kind="line", ax=ax3, label=country)

plt.legend()
plt.show()

# fig3, ax3 = plt.subplots(figsize=(8, 6))

# for reg in main_region_filters:
#     reg.plot(kind="line", ax=ax3, label=reg["Headquarters Location"])


# How many are actively hiring

# Funding amount

# # Create a bar graph
# grouped_data.plot(kind='bar')
# plt.title('Bar Graph')
# plt.xlabel('X Label')
# plt.ylabel('Y Label')
# plt.show()

# # Create a line graph
