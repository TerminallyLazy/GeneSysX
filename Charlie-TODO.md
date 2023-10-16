Chat History Architecture

*Save Session state variables of chat cycle.
** Either through Streamlit
** Through Json
**** Json could have a type [ Message, Dataframe, Image, Visualizaiton ]
**** For Dataframes, Visualizations it could have a link to the Visualizer and Image which could be pulled down from S3.
**** Dataframe messages could have relevant info we would want to feed to chat gpt. (Column Names, column types )
**** If they want to work a data frame again. We would have to have the gpt model search through json, pull down the dataframe, display a loading message, then call smart dataframe. This could be a ton of work but it will be worth it.
**** The messages(text) could be served in the json itself.
******** I like the json approach because I transition this to other architectures and its readable *****
**** Right now just append it but in the future [Build out Function wrappers to append to these json structures. 
**** Chat session lists json could be formatted with the user_id at the top and the name of the json could be user id
So the Json structure could be:

s3:gensys/
--user_id/
--user_id/
  --user_id_sessions.json
      {session_id
         { csv_file {
            location: 's3:gensys/user_id/datasets/abc-time.csv'
            unix-time:
            "metadata": {
                "columns": {
                    "Name": "A"
                    "Type": dtype
                    "Possible-Values": unique_values.list()
                }
            }
           message: ['some text here', time]
           response: ['some other text here', time]
           message: ['some text here', time],
           dataset: [s3:gensys/user_id/datasets/abc-time.csv, time],
           visualization: s3 
	 }
  --user-id-datasets/
    --abc-time.csv