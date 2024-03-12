/*
   Copyright 2022 SECO Mind srl

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/

import React, { createContext, useContext, useMemo } from "react";

import AstarteClient from "../AstarteClient";

type AstarteControls = {
  astarteClient: AstarteClient;
  deviceId: string;
};

type AstarteProviderProps = {
  astarteUrl: URL;
  children: React.ReactNode;
  deviceId: string;
  realm: string;
  token: string;
};

const AstarteContext = createContext<AstarteControls | null>(null);

const AstarteProvider = ({
  astarteUrl,
  children,
  deviceId,
  realm,
  token,
}: AstarteProviderProps) => {
  const astarteClient = useMemo(() => {
    return new AstarteClient({ astarteUrl, realm, token });
  }, [astarteUrl, realm, token]);

  const providerValue: AstarteControls = useMemo(() => {
    return { astarteClient, deviceId };
  }, [astarteClient, deviceId]);

  return (
    <AstarteContext.Provider value={providerValue}>
      {children}
    </AstarteContext.Provider>
  );
};

const useAstarte = (): AstarteControls => {
  const context = useContext(AstarteContext);
  if (context === null) {
    throw new Error("useAstarte must be used within an AstarteProvider");
  }
  return context;
};

export { useAstarte };

export default AstarteProvider;
