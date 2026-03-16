$RG = "<your-resource-group-name>"
# get the RG tags
$tags = az group show -n $RG --query tags
$tags 
# add a tag to the resource group
az group update -n $RG --set tags.apiKeyEnabled=true

$accountName = "<your-account-name>"
az cognitiveservices account list -g $RG > extract.txt
$rid = az cognitiveservices account show -n $accountName -g $RG --query id -o tsv
az resource update --ids $rid --set properties.disableLocalAuth=false