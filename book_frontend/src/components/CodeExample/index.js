import React from 'react';
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import CodeBlock from '@theme/CodeBlock';

import styles from './styles.module.css';

function CodeExample({title, pythonCode, explanation, output}) {
  return (
    <div className={styles.codeExampleContainer}>
      <h4>{title}</h4>
      <Tabs>
        <TabItem value="python" label="Python">
          <CodeBlock language="python">{pythonCode}</CodeBlock>
        </TabItem>
      </Tabs>
      {explanation && (
        <div className={styles.explanation}>
          <strong>Explanation:</strong> {explanation}
        </div>
      )}
      {output && (
        <div className={styles.output}>
          <strong>Output:</strong>
          <CodeBlock language="bash">{output}</CodeBlock>
        </div>
      )}
    </div>
  );
}

export default CodeExample;