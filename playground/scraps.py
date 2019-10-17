# def run():
#     log_groups = None
#     run_count = 0

#     while True:
#         response = client.describe_log_groups()
#         new_log_groups = response["logGroups"]
#         log_group_names = [log_group["logGroupName"] for log_group in new_log_groups]

#         run_count = run_count + 1
#         print(f"Run: {run_count}")
#         if log_groups is None:
#             log_groups = "safas"
#             log_groups = new_log_groups
#             print("First Run")
#             time.sleep(1)
#         else:
#             print(len(log_groups))

#             if len(new_log_groups) > len(log_groups):
#                 log_groups = new_log_groups
#                 print("Hey now we think they are more log groups!")
#                 time.sleep(1)
#                 if run_count > 2:
#                     # New Tmux window with Log Group
#                     command = "tmux split-window -h python logs.py"
#                     process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
#                     output, error = process.communicate()
#             else:
#                 log_groups = new_log_groups
#                 print("Sleeping")
#                 time.sleep(1)
