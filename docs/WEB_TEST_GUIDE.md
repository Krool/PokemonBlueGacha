# Web Version Testing Guide

## 🎮 Test the Web Build

The web version has been built and is ready for testing with the new audio fixes!

---

## Local Testing (In Progress)

### Server Running
```bash
pygbag src/main.py
```

The game should now be accessible at: **http://localhost:8000**

---

## 🧪 Testing Checklist for Audio Fixes

### ✅ Initial Load Test
1. Open http://localhost:8000 in your browser
2. Watch the browser console (F12 → Console tab)
3. **Expected Output:**
   ```
   ✓ Audio mixer initialized
     Set up 8 audio channels for web compatibility
     Note: Audio may require user interaction to start (browser policy)
   ...
   ⏸ Music queued (waiting for user interaction): backgroundX.mp3
   ```

### ✅ User Interaction Test
4. Click anywhere on the screen OR press any key
5. **Expected Output in Console:**
   ```
   ✓ User interaction detected - audio enabled
     Playing pending music: backgroundX.mp3
   ```
6. **Expected Behavior:** Music should start playing immediately

### ✅ Sound Effects Test
7. Add gold (click the currency display)
8. Click "OPEN GACHA"
9. Perform a single pull
10. **Expected:** Should hear roll sound effects (roll1/2/3 or legendary)
11. **Expected:** Animation sound plays without delay

### ✅ Music Continuity Test
12. Navigate between states (Inventory → Gacha → back to Inventory)
13. **Expected:** Music continues playing without interruption
14. **Expected:** No additional "user interaction" prompts

### ✅ Mute/Unmute Test
15. Click the "MUTE" button in inventory
16. **Expected:** Music stops
17. Click "UNMUTE"
18. **Expected:** Random background music starts immediately (no interaction needed)

### ✅ Legendary Pull Test
19. Add gold, do pulls until you get a legendary
20. **Expected:** Hear both "legendary" AND "chaching" sounds together
21. **Expected:** No audio lag or stuttering

---

## 🌐 Browser Compatibility Tests

Test in multiple browsers to ensure audio works correctly:

### Chrome/Edge (Chromium)
- ✅ Should work perfectly
- Autoplay policy: Requires user interaction

### Firefox
- ✅ Should work perfectly  
- Autoplay policy: Requires user interaction

### Safari (Desktop)
- ⚠️ Test carefully
- Autoplay policy: Strictest browser
- May need multiple clicks to start audio

### Mobile Chrome/Safari
- ⚠️ Touch input required
- Tap anywhere to start audio
- Test sound effects work on tap

---

## 🐛 Known Issues to Watch For

### If Music Doesn't Start:
1. Check browser console for errors
2. Verify file paths are correct
3. Try clicking multiple times
4. Try pressing a key instead of clicking
5. Check browser autoplay settings

### If Sound Effects Don't Play:
1. Check console for "Sound not loaded" warnings
2. Verify all `.mp3` files are in build
3. Check network tab (F12) for failed file loads

### If Audio Lags:
1. This is expected on first play (loading)
2. Subsequent sounds should be faster
3. Monitor memory usage in performance tab

---

## 📊 Performance Monitoring

Open browser DevTools (F12) and check:

### Console Tab
- Look for any error messages
- Verify all audio files loaded successfully
- Check for repeated init messages (shouldn't happen)

### Network Tab
- Verify all MP3 files load (200 status)
- Check file sizes are reasonable
- Monitor loading times

### Performance Tab
- Watch memory usage (shouldn't grow indefinitely)
- Check frame rate (should be stable ~60 FPS)
- Monitor audio context state

---

## ✅ Success Criteria

Your audio system is working correctly if:

1. ✅ Console shows "Music queued" message on load
2. ✅ First click/keypress triggers audio
3. ✅ Music plays immediately after interaction
4. ✅ Sound effects work during gacha pulls
5. ✅ Music continues between state changes
6. ✅ Mute/unmute works correctly
7. ✅ No duplicate mixer initialization messages
8. ✅ No audio-related errors in console
9. ✅ Performance remains stable

---

## 🎯 What to Look For in Console

### Good Output (Desktop-like behavior still works):
```
============================================================
POKÉMON BLUE GACHA - Initializing...
============================================================

Initializing managers...
✓ Audio mixer initialized

Loading game data...
✓ Loaded 151 Pokémon from data/pokemon_gen1.csv
✓ Loaded 15 types from data/pokemon_types.csv
✓ Loaded 5 rarities from data/rarity_drop_weights.csv
...
```

### Good Output (Web-specific behavior):
```
✓ Audio mixer initialized
  Set up 8 audio channels for web compatibility
  Note: Audio may require user interaction to start (browser policy)
...
⏸ Music queued (waiting for user interaction): background3.mp3
[User clicks]
✓ User interaction detected - audio enabled
  Playing pending music: background3.mp3
```

### Bad Output (Problems to fix):
```
❌ Audio initialization failed: [error]
❌ pygame.error: mixer not initialized
❌ Warning: Sound file not found: Assets/Sounds/roll1.mp3
❌ Error playing sound roll1: [error]
```

---

## 🔧 Quick Fixes

### If Audio Completely Fails
1. Check browser supports Web Audio API
2. Clear browser cache (Ctrl+Shift+Delete)
3. Try incognito/private mode
4. Update browser to latest version

### If Music Never Plays
1. Check browser console for pygame errors
2. Verify MP3 files are in build/web folder
3. Try different browser
4. Check browser autoplay settings (chrome://settings/content/sound)

### If First Interaction Doesn't Work
1. Try multiple clicks
2. Try pressing different keys
3. Check browser is focused
4. Reload page and try again

---

## 📝 Report Results

After testing, document:

1. **Browser & Version:** e.g., Chrome 120.0
2. **First Load:** Did music queue? ✅/❌
3. **User Interaction:** Did audio start? ✅/❌
4. **Sound Effects:** Working? ✅/❌
5. **State Transitions:** Music continues? ✅/❌
6. **Console Errors:** Any errors? List them
7. **Performance:** FPS stable? Memory OK?

---

## 🚀 Next Steps After Testing

### If All Tests Pass:
1. ✅ Build is ready for deployment
2. Deploy to GitHub Pages or Itch.io
3. Share the link!

### If Tests Fail:
1. Document specific failures
2. Check console errors
3. Test in different browser
4. Report issues for fixing

---

## 🎊 Expected Experience

**Player's perspective:**
1. Game loads with nice loading screen
2. Music indicator shows "Loading..." or queued message
3. Player naturally clicks or presses space
4. Music starts smoothly
5. Rest of game works perfectly
6. No weird delays or interruptions

**Developer's perspective:**
1. Clean console output
2. No errors
3. Audio system initialized correctly
4. User interaction detected properly
5. All sounds load successfully
6. Memory stable, performance good

---

## 📞 Need Help?

If you encounter issues:
1. Check console for error messages
2. Review `docs/AUDIO_SYSTEM_FIXES.md` for technical details
3. Test on different browser
4. Clear cache and try again
5. Check network tab for failed file loads

---

**Happy Testing! 🎮🎵**

