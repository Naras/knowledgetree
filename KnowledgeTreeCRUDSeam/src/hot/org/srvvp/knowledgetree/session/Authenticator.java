package org.srvvp.knowledgetree.session;

import javax.ejb.Local;

@Local
public interface Authenticator {

	boolean authenticate();

}
