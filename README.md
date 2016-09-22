# iOS-Project-Build-Time-Analyzer
More detailed build time measuring tool for iOS projects.


## Example usage
### Enable detailed build logs
```
defaults write com.apple.dt.xcodebuild CommandLineBuildTimingLogLevel -int 5
```

### Generate build.log
```
script -q /dev/null xcodebuild clean build -workspace brainly.xcworkspace -scheme Brainly -destination "platform=iOS Simulator,name=iPhone 5s" | grep CommandLineBuildTiming | cut -d " " -f 6- | grep -v REAL | sed -e 's/|//' > build.log
```

### Use python script to parse output build output
```
python parse_build_log.py ./Example/build.log
```
