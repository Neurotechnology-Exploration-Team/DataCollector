using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEditor;
using UnityEngine.UI;

public class ActionController : MonoBehaviour
{
    public Sprite Blink;
    public Sprite EyesOpen;
    public Sprite EyesClosed;
    public Sprite BrowDown;
    public Sprite BrowUp;
    public Sprite Stop;
    public Sprite Select;
    public Sprite Left;
    public Sprite Right;
    public Sprite Down;
    public Sprite Up;
    public Sprite Empty;

    public List<Sprite> ImageSchedule;
    public List<string> ImageScheduleNames;
    public List<float> ImageScheduleTimes;

    public enum TRIALTYPE
    {
        SWITCHING,
        CONST
    }
    public TRIALTYPE TrialType = TRIALTYPE.CONST;
    public Image Attached;
    public string AttachedMode = "Empty";
    public AudioSource Player;
    public int ImageIndex = 0;
    public bool Active = false;
    public float time = 0.0f;
    public float MaxTime = 160.0f;
    public int MinTrials = 20;
    public bool ending = false;

    public ActionStateOutlet Outlet;

    // Start is called before the first frame update
    void Awake()
    {
        Attached = GetComponent<Image>();
        Blink       = Resources.Load<Sprite>("Images/Blink");
        EyesOpen     = Resources.Load<Sprite>("Images/EyesOpen");
        EyesClosed   = Resources.Load<Sprite>("Images/EyesClosed");
        BrowDown    = Resources.Load<Sprite>("Images/BrowFurrow");
        BrowUp      = Resources.Load<Sprite>("Images/BrowUnfurrow");
        Stop        = Resources.Load<Sprite>("Images/Stop");
        Select      = Resources.Load<Sprite>("Images/Select");
        Left        = Resources.Load<Sprite>("Images/Left");
        Right       = Resources.Load<Sprite>("Images/Right");
        Down        = Resources.Load<Sprite>("Images/Down");
        Up          = Resources.Load<Sprite>("Images/Up");
        Empty       = Resources.Load<Sprite>("Images/Empty");
        ImageSchedule = new List<Sprite>();
        ImageScheduleNames = new List<string>();
        ImageScheduleTimes = new List<float>();
        ending = false;
    }

    private void OnDestroy()
    {
        Resources.UnloadAsset(Blink);
        Resources.UnloadAsset(EyesOpen);
        Resources.UnloadAsset(EyesClosed);
        Resources.UnloadAsset(BrowDown);
        Resources.UnloadAsset(BrowUp);
        Resources.UnloadAsset(Stop);
        Resources.UnloadAsset(Select);
        Resources.UnloadAsset(Left);
        Resources.UnloadAsset(Right);
        Resources.UnloadAsset(Down);
        Resources.UnloadAsset(Up);
        Resources.UnloadAsset(Empty);
    }

    // Update is called once per frame
    void LateUpdate()
    {
        if (Active)
        {
            time += Time.deltaTime;
            UpdateImage();
            if (time > MaxTime && !ending)
                End();
        }
    }

    private void UpdateImage()
    {
        if (ImageScheduleTimes.Count == 0 || !Active) {
            Attached.sprite = Empty;
            AttachedMode = "Empty";
            Outlet.RequestSample("Empty");
            return;
        }
        if (time > ImageScheduleTimes[0])
        {
            Attached.sprite = ImageSchedule[0];
            if (AttachedMode != ImageScheduleNames[0] && TrialType==TRIALTYPE.SWITCHING)
            {
                Player.PlayOneShot(Player.clip,1.0f);
            }
            AttachedMode = ImageScheduleNames[0];
            Debug.Log(ImageScheduleNames[0]);
            ImageSchedule.RemoveAt(0);
            ImageScheduleTimes.RemoveAt(0);
            ImageScheduleNames.RemoveAt(0);
            Outlet.RequestSample("Empty");
        }
    }

#if UNITY_EDITOR
    private void toggleInEditor(bool on)
    {
        EditorApplication.ExecuteMenuItem("Window/General/Game");
        EditorWindow window = EditorWindow.focusedWindow;
        // Assume the game view is focused.
        window.maximized = on;
    }
#endif

    private void End()
    {
        Outlet.RequestSample("END");
        StartCoroutine("TrialEnder");
    }

    private IEnumerator TrialEnder()
    {
        if (ending)
            yield return null;
        else {
            ending = true;
            yield return new WaitForSeconds(5.0f);
            Active = false;
            Outlet.RequestSample("5sWaitOver");

    #if UNITY_EDITOR
            toggleInEditor(false);
    #endif
            time = 0.0f;
            ImageSchedule = new List<Sprite>();
            ImageScheduleNames = new List<string>();
            ImageScheduleTimes = new List<float>();
    #if UNITY_EDITOR
            EditorUtility.DisplayDialog("Trial Complete!",
                "Please click ok and you may end the LSL Stream Recording for this trial.",
                "OK");
    #endif
            ending = false;
            yield return null;
        }
        yield return null;
    }

    public void StartTrial()
    {
#if UNITY_EDITOR
        toggleInEditor(true);
#endif
        Outlet.RequestSample("5sWaitStart");
        StartCoroutine("TrialActivator");
        ending = false;
    }

    public IEnumerator TrialActivator()
    {
        yield return new WaitForSeconds(5.0f);
        Active = true;
        time = 0.0f;
        Attached.sprite = Empty;
        AttachedMode = "Empty";
        Outlet.RequestSample("START");
        yield return null;
    }
    #region Switch Trials
    public void SetBlinkTrial()
    {
        GenerateBlinkingTrial(Blink, "Blink", Empty, "Empty");
    }
    public void SetEyeOpenCloseTrial()
    {
        GenerateSwitchingTrial(EyesOpen, "Eye Open", EyesClosed, "Eye Closed");
    }
    public void SetBrowFurrowUnfurrowTrial()
    {
        GenerateSwitchingTrial(BrowDown, "Brow Furrow", BrowUp, "Brow Up");
    }
    public void SetStopToUpTrial()
    {
        GenerateSwitchingTrial(Stop, "Stop", Up, "Float Up");
    }
    public void SetStopToDownTrial()
    {
        GenerateSwitchingTrial(Stop, "Stop", Down, "Float Down");
    }
    public void SetStopToLeftTrial()
    {
        GenerateSwitchingTrial(Stop, "Stop", Left, "Float Left");
    }
    public void SetStopToRightTrial()
    {
        GenerateSwitchingTrial(Stop, "Stop", Right, "Float Right");
    }
    public void SetStopToSelectTrial()
    {
        GenerateSwitchingTrial(Stop, "Stop", Select, "Select");
    }
    #endregion
    #region Const Trial
    public void SetEyeOpenTrial()
    {
        GenerateConstTrial(EyesOpen, "Eye Open");
    }
    public void SetEyeClosedTrial()
    {
        GenerateConstTrial(EyesClosed, "Eye Closed");
    }
    public void SetBrowFurrowedTrial()
    {
        GenerateConstTrial(BrowDown, "Brow Furrow");
    }
    public void SetBrowUnfurrowedTrial()
    {
        GenerateConstTrial(BrowUp, "Brow Unfurrowed");
    }
    public void SetStopTrial()
    {
        GenerateConstTrial(Stop, "Stop");
    }
    public void SetLeftTrial()
    {
        GenerateConstTrial(Left, "Float Left");
    }
    public void SetRightTrial()
    {
        GenerateConstTrial(Right, "Float Right");
    }
    public void SetUpTrial()
    {
        GenerateConstTrial(Up, "Float Up");
    }
    public void SetDownTrial()
    {
        GenerateConstTrial(Down, "Float Down");
    }
    public void SetSelectTrial()
    {
        GenerateConstTrial(Select, "Select");
    }
    #endregion
    public void GenerateConstTrial(Sprite a, string aName)
    {
        TrialType = TRIALTYPE.CONST;
        float iTime = 0.0f;
        float minTime = 2.5f;
        float maxTime = 6.0f;
        ImageSchedule = new List<Sprite>();
        ImageScheduleTimes = new List<float>();
        ImageScheduleNames = new List<string>();
        ImageSchedule.Add(a);
        ImageScheduleTimes.Add(0.0f);
        ImageScheduleNames.Add(aName);
        for (int i = 0; i < MinTrials*2; i++)
        {
            iTime += Random.Range(minTime, maxTime);
            ImageSchedule.Add(a);
            ImageScheduleTimes.Add(iTime);
            ImageScheduleNames.Add(aName);

        }
        MaxTime = iTime + 10.0f;
    }
    public void GenerateSwitchingTrial(Sprite a, string aName, Sprite b, string bName)
    {
        TrialType = TRIALTYPE.SWITCHING;
        float iTime = 0.0f;
        float minTime = 2.5f;
        float maxTime = 6.0f;

        ImageSchedule = new List<Sprite>();
        ImageScheduleTimes = new List<float>();
        ImageScheduleNames = new List<string>();
        ImageSchedule.Add(Empty);
        ImageScheduleTimes.Add(0.0f);
        ImageScheduleNames.Add("Empty");
        for (int i = 0; i<MinTrials; i++)
        {
            iTime += Random.Range(minTime, maxTime);
            ImageSchedule.Add(a);
            ImageScheduleTimes.Add(iTime);
            ImageScheduleNames.Add(aName);

            iTime += Random.Range(minTime, maxTime);
            ImageSchedule.Add(b);
            ImageScheduleTimes.Add(iTime);
            ImageScheduleNames.Add(bName);
        }
        MaxTime = iTime + 10.0f;
    }

    public void GenerateBlinkingTrial(Sprite a, string aName, Sprite b, string bName)
    {
        TrialType = TRIALTYPE.SWITCHING;
        float iTime = 0.0f;
        float minTime = 2.5f;
        float maxTime = 6.0f;

        ImageSchedule = new List<Sprite>();
        ImageScheduleTimes = new List<float>();
        ImageScheduleNames = new List<string>();
        ImageSchedule.Add(Empty);
        ImageScheduleTimes.Add(0.0f);
        ImageScheduleNames.Add("Empty");
        for (int i = 0; i < MinTrials; i++)
        {
            iTime += Random.Range(minTime, maxTime);
            ImageSchedule.Add(a);
            ImageScheduleTimes.Add(iTime);
            ImageScheduleNames.Add(aName);

            iTime += (1.0f);
            ImageSchedule.Add(b);
            ImageScheduleTimes.Add(iTime);
            ImageScheduleNames.Add(bName);
        }
        MaxTime = iTime + 10.0f;
    }
}

[CustomEditor(typeof(ActionController))]
public class ActionCtrlEditor : Editor {
    bool ShowHidden = false;
    public override void OnInspectorGUI()
    {
        ActionController def = (ActionController)target;
        if (!def.Active)
        {
            GUI.backgroundColor = Color.green;
            GUILayout.Label("Select a Trial Type. Then begin a Trial.");
            GUILayout.BeginHorizontal();
            GUILayout.BeginVertical();
            if (GUILayout.Button("SetBlinkTrial"))
            {
                def.SetBlinkTrial();
            }
            else if (GUILayout.Button("SetEyeOpenCloseTrial"))
            {
                def.SetEyeOpenCloseTrial();
            }
            else if (GUILayout.Button("SetBrowFurrowUnfurrowTrial"))
            {
                def.SetBrowFurrowUnfurrowTrial();
            }
            else if (GUILayout.Button("SetStopToUpTrial"))
            {
                def.SetStopToUpTrial();
            }
            else if (GUILayout.Button("SetStopToDownTrial"))
            {
                def.SetStopToDownTrial();
            }
            else if (GUILayout.Button("SetStopToLeftTrial"))
            {
                def.SetStopToLeftTrial();
            }
            else if (GUILayout.Button("SetStopToRightTrial"))
            {
                def.SetStopToRightTrial();
            }
            else if (GUILayout.Button("SetStopToSelectTrial"))
            {
                def.SetStopToSelectTrial();
            }
            else if (GUILayout.Button("SetBrowFurrowedTrial"))
            {
                def.SetBrowFurrowedTrial();
            }
            GUILayout.EndVertical();
            GUILayout.BeginVertical();
            if (GUILayout.Button("SetStopTrial"))
            {
                def.SetStopTrial();
            }
            else if (GUILayout.Button("SetLeftTrial"))
            {
                def.SetLeftTrial();
            }
            else if (GUILayout.Button("SetRightTrial"))
            {
                def.SetRightTrial();
            }
            else if (GUILayout.Button("SetUpTrial"))
            {
                def.SetUpTrial();
            }
            else if (GUILayout.Button("SetDownTrial"))
            {
                def.SetDownTrial();
            }
            else if (GUILayout.Button("SetSelectTrial"))
            {
                def.SetSelectTrial();
            }
            else if (GUILayout.Button("SetEyeOpenTrial"))
            {
                def.SetEyeOpenTrial();
            }
            else if (GUILayout.Button("SetEyeClosedTrial"))
            {
                def.SetEyeClosedTrial();
            }
            else if (GUILayout.Button("SetBrowUnfurrowedTrial"))
            {
                def.SetBrowUnfurrowedTrial();
            }
            GUILayout.EndVertical();
            GUILayout.EndHorizontal();

            EditorGUILayout.BeginVertical();
            if (GUILayout.Button("Start Trial!",GUILayout.Height(48)))
            {
                def.StartTrial();
            }
            EditorGUILayout.EndVertical();
        }
        else
        {
            GUI.backgroundColor = Color.red;
            GUILayout.Label("Set Activation is Not Allowed...\nPlease complete the current trial.");
        }

        if (GUILayout.Button("Play Sound") && Application.isPlaying) {
            def.Player.PlayOneShot(def.Player.clip, 1.0f);
        }
        ShowHidden = (GUILayout.Button((ShowHidden)?"Hide":"Show Hidden")) ? !ShowHidden : ShowHidden;
        if(ShowHidden)
            DrawDefaultInspector();
        serializedObject.ApplyModifiedProperties();
    }
}
