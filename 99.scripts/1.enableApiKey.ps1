$RG = "<your-resource-group-name>"
$accountName = "<your-account-name>"
az cognitiveservices account list -g $RG > extract.txt
$rid = az cognitiveservices account show -n $accountName -g $RG --query id -o tsv
az resource update --ids $rid --set properties.disableLocalAuth=false