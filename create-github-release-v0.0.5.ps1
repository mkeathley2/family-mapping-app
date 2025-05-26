# PowerShell script to create GitHub release v0.0.5
# This will trigger the GitHub Actions workflow to build all platforms

$repo = "mkeathley2/family-mapping-app"
$tag = "v0.0.5"
$title = "Family Mapping App v0.0.5 - Cross-Platform Standalone Support"

# Read release notes
$releaseNotes = Get-Content -Path "RELEASE_NOTES_v0.0.5.md" -Raw

# Create release data
$releaseData = @{
    tag_name = $tag
    target_commitish = "master"
    name = $title
    body = $releaseNotes
    draft = $false
    prerelease = $false
} | ConvertTo-Json -Depth 10

Write-Host "Creating GitHub release $tag..."
Write-Host "Repository: $repo"
Write-Host "Title: $title"
Write-Host ""

# GitHub API endpoint
$uri = "https://api.github.com/repos/$repo/releases"

try {
    # Create the release
    $response = Invoke-RestMethod -Uri $uri -Method Post -Body $releaseData -ContentType "application/json"
    
    Write-Host "✓ Release created successfully!" -ForegroundColor Green
    Write-Host "Release URL: $($response.html_url)" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "GitHub Actions should now be building cross-platform packages automatically."
    Write-Host "Check the Actions tab in your GitHub repository to monitor progress."
    Write-Host ""
    Write-Host "Once complete, the following files will be available for download:"
    Write-Host "- family-mapping-app-standalone-windows-v0.0.5.zip"
    Write-Host "- family-mapping-app-standalone-macos-v0.0.5.zip"
    Write-Host "- family-mapping-app-standalone-linux-v0.0.5.tar.gz"
    
} catch {
    Write-Host "❌ Error creating release:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    Write-Host "You can create the release manually by:"
    Write-Host "1. Going to https://github.com/$repo/releases/new"
    Write-Host "2. Setting tag to: $tag"
    Write-Host "3. Setting title to: $title"
    Write-Host "4. Copying the content from RELEASE_NOTES_v0.0.5.md"
    Write-Host "5. Publishing the release"
}

Write-Host ""
Write-Host "Press any key to continue..."
Read-Host 