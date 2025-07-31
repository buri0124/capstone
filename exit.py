

if __name__ == "__main__":
    # Simulate exit events and export to CSV
    vc_exit_df = pd.DataFrame(vc_exit_events)
    vc_exit_df.to_csv("vc_exit.csv", index=False)
